import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from django.conf import settings
from rest_framework import status


class Command(BaseCommand):
    help = 'Create sample movie data using the same flow as the test case'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-file',
            type=str,
            default='sample_movie_data.json',
            help='Path to the JSON file containing sample data'
        )
        parser.add_argument(
            '--admin-username',
            type=str,
            default='cms',
            help='Username for admin user (default: cms)'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='admin123#',
            help='Password for admin user (default: admin123#)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting sample movie data creation...'))
        
        # Load data from JSON file
        data_file_path = self.get_data_file_path(options['data_file'])
        sample_data = self.load_sample_data(data_file_path)
        
        # Create or get admin user
        admin_user = self.get_or_create_admin_user(
            options['admin_username'], 
            options['admin_password']
        )
        
        # Initialize client and authenticate
        client = Client()
        client.force_login(admin_user)
        
        try:
            movies_created = 0
            movies_data = sample_data.get('movies', [])
            
            if not movies_data:
                self.stdout.write(self.style.ERROR('❌ No movies found in data file'))
                return
            
            self.stdout.write(f'📽️  Found {len(movies_data)} movies to process...')
            
            for i, movie_data in enumerate(movies_data, 1):
                self.stdout.write(f'\n--- Processing Movie {i}/{len(movies_data)}: {movie_data["moviemedia"]["name"]} ---')
                
                try:
                    # Create movie media
                    moviemedia_slug = self.create_moviemedia(client, movie_data['moviemedia'])
                    
                    # Create cast media and cast entries
                    cast_ids = []
                    for cast_data in movie_data.get('cast', []):
                        castmedia_id = self.create_castmedia(client, cast_data['castmedia'])
                        cast_id = self.create_cast(client, cast_data['castmedia']['name'])
                        cast_ids.append(cast_id)
                    
                    # Create creator media and creator entries
                    creator_ids = []
                    for creator_data in movie_data.get('creators', []):
                        creatormedia_id = self.create_creatormedia(client, creator_data['creatormedia'])
                        creator_id = self.create_creator(client, creator_data['creatormedia']['name'])
                        creator_ids.append(creator_id)
                    
                    # Create writer media and writer entries
                    writer_ids = []
                    for writer_data in movie_data.get('writers', []):
                        writermedia_id = self.create_writermedia(client, writer_data['writermedia'])
                        writer_id = self.create_writer(client, writer_data['writermedia']['name'])
                        writer_ids.append(writer_id)
                    
                    # Create platform
                    platform_id = self.create_platform(client, movie_data['platform'])
                    
                    # Create genres
                    genre_ids = []
                    for genre_data in movie_data.get('genres', []):
                        genre_id = self.create_genre(client, genre_data)
                        genre_ids.append(genre_id)
                    
                    # Create final movie
                    movie_id = self.create_movie(
                        client, moviemedia_slug, genre_ids, platform_id, 
                        cast_ids, creator_ids, writer_ids
                    )
                    
                    movies_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Successfully created movie "{movie_data["moviemedia"]["name"]}" with ID: {movie_id}')
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error creating movie "{movie_data["moviemedia"]["name"]}": {str(e)}')
                    )
                    continue
            
            self.stdout.write(f'\n🎬 Summary: Successfully created {movies_created}/{len(movies_data)} movies!')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error processing sample data: {str(e)}')
            )
            raise e

    def get_data_file_path(self, filename):
        """Get the full path to the data file"""
        if os.path.isabs(filename):
            return filename
        
        # Look for the file in management/commands/data/ directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        return os.path.join(data_dir, filename)

    def load_sample_data(self, file_path):
        """Load sample data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'❌ Data file not found: {file_path}')
            )
            self.stdout.write(
                self.style.WARNING('Please ensure the JSON file exists in the correct location.')
            )
            raise
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Invalid JSON in data file: {e}')
            )
            raise

    def get_or_create_admin_user(self, username, password):
        """Create or get admin user"""
        User = get_user_model()
        try:
            admin_user = User.objects.get(username=username)
            self.stdout.write(f'✅ Using existing admin user: {username}')
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username=username,
                password=password,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'✅ Created new admin user: {username}')
        
        return admin_user

    def create_moviemedia(self, client, data):
        """Create or get movie media entry"""
        url = reverse('movie-media-create')
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            slug = response.json()['movie_slug']
            self.stdout.write(f'✅ MovieMedia created with slug: {slug}')
            return slug
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Check if it's a duplicate error, try to get existing
            response_data = response.json()
            if 'name' in response_data and 'already exists' in str(response_data).lower():
                # Try to get existing moviemedia by name
                existing_slug = self.get_existing_moviemedia_by_name(client, data['name'])
                if existing_slug:
                    self.stdout.write(f'✅ Using existing MovieMedia with slug: {existing_slug}')
                    return existing_slug
        
        self.stdout.write(f'❌ Failed to create MovieMedia: {response.status_code}')
        self.stdout.write(f'Response: {response.content.decode()}')
        raise Exception(f'Failed to create MovieMedia: {response.status_code}')

    def create_castmedia(self, client, data):
        """Create or get cast media entry"""
        url = reverse('cast-media-create')
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            cast_id = response.json()['id']
            self.stdout.write(f'✅ CastMedia created with ID: {cast_id}')
            return cast_id
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Try to get existing castmedia by name
            existing_id = self.get_existing_castmedia_by_name(client, data['name'])
            if existing_id:
                self.stdout.write(f'✅ Using existing CastMedia with ID: {existing_id}')
                return existing_id
        
        raise Exception(f'Failed to create CastMedia: {response.status_code}')

    def create_creatormedia(self, client, data):
        """Create or get creator media entry"""
        url = reverse('creator-media-create')
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            creator_id = response.json()['id']
            self.stdout.write(f'✅ CreatorMedia created with ID: {creator_id}')
            return creator_id
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Try to get existing creatormedia by name
            existing_id = self.get_existing_creatormedia_by_name(client, data['name'])
            if existing_id:
                self.stdout.write(f'✅ Using existing CreatorMedia with ID: {existing_id}')
                return existing_id
        
        raise Exception(f'Failed to create CreatorMedia: {response.status_code}')

    def create_writermedia(self, client, data):
        """Create or get writer media entry"""
        url = reverse('writer-media-create')
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            writer_id = response.json()['id']
            self.stdout.write(f'✅ WriterMedia created with ID: {writer_id}')
            return writer_id
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Try to get existing writermedia by name
            existing_id = self.get_existing_writermedia_by_name(client, data['name'])
            if existing_id:
                self.stdout.write(f'✅ Using existing WriterMedia with ID: {existing_id}')
                return existing_id
        
        raise Exception(f'Failed to create WriterMedia: {response.status_code}')

    def create_platform(self, client, data):
        """Create or get platform entry"""
        url = reverse('platform-list-create')
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            platform_id = response.json()['id']
            self.stdout.write(f'✅ Platform created with ID: {platform_id}')
            return platform_id
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Try to get existing platform by name
            existing_id = self.get_existing_platform_by_name(client, data['platform'])
            if existing_id:
                self.stdout.write(f'✅ Using existing Platform with ID: {existing_id}')
                return existing_id
        
        raise Exception(f'Failed to create Platform: {response.status_code}')

    def create_genre(self, client, data):
        """Create or get genre entry"""
        url = reverse('genre-list-create')
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            genre_id = response.json()['id']
            self.stdout.write(f'✅ Genre created with ID: {genre_id}')
            return genre_id
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Try to get existing genre by name
            existing_id = self.get_existing_genre_by_name(client, data['name'])
            if existing_id:
                self.stdout.write(f'✅ Using existing Genre with ID: {existing_id}')
                return existing_id
        
        raise Exception(f'Failed to create Genre: {response.status_code}')

    def create_cast(self, client, castmedia_name):
        """Create or get cast entry"""
        url = reverse('cast-create-list')
        data = {"castmedia": castmedia_name}
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            cast_id = response.json()['id']
            self.stdout.write(f'✅ Cast created with ID: {cast_id}')
            return cast_id
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Try to get existing cast by castmedia name
            existing_id = self.get_existing_cast_by_castmedia(client, castmedia_name)
            if existing_id:
                self.stdout.write(f'✅ Using existing Cast with ID: {existing_id}')
                return existing_id
        
        raise Exception(f'Failed to create Cast: {response.status_code}')

    def create_creator(self, client, creatormedia_name):
        """Create or get creator entry"""
        url = reverse('creator-list-create')
        data = {"creatormedia": creatormedia_name}
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            creator_id = response.json()['id']
            self.stdout.write(f'✅ Creator created with ID: {creator_id}')
            return creator_id
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Try to get existing creator by creatormedia name
            existing_id = self.get_existing_creator_by_creatormedia(client, creatormedia_name)
            if existing_id:
                self.stdout.write(f'✅ Using existing Creator with ID: {existing_id}')
                return existing_id
        
        raise Exception(f'Failed to create Creator: {response.status_code}')

    def create_writer(self, client, writermedia_name):
        """Create or get writer entry"""
        url = reverse('writer-list-create')
        data = {"writermedia": writermedia_name}
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            writer_id = response.json()['id']
            self.stdout.write(f'✅ Writer created with ID: {writer_id}')
            return writer_id
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            # Try to get existing writer by writermedia name
            existing_id = self.get_existing_writer_by_writermedia(client, writermedia_name)
            if existing_id:
                self.stdout.write(f'✅ Using existing Writer with ID: {existing_id}')
                return existing_id
        
        raise Exception(f'Failed to create Writer: {response.status_code}')

    def create_movie(self, client, moviemedia_slug, genre_ids, platform_id, cast_ids, creator_ids, writer_ids):
        """Create the final movie entry"""
        url = reverse('movie-list-create')
        data = {
            "moviemedia": moviemedia_slug,
            "movie_genre_ids": genre_ids,
            "platform_id": platform_id,
            "movie_cast_ids": cast_ids,
            "movie_creator_ids": creator_ids,
            "movie_writer_ids": writer_ids
        }
        
        response = client.post(url, data, content_type='application/json')
        
        if response.status_code == status.HTTP_201_CREATED:
            movie_id = response.json().get('id', 'Unknown')
            self.stdout.write(f'✅ Movie created with ID: {movie_id}')
            return movie_id
        else:
            self.stdout.write(f'❌ Failed to create Movie: {response.status_code}')
            self.stdout.write(f'Response: {response.content.decode()}')
            raise Exception(f'Failed to create Movie: {response.status_code}')

    # Helper methods to get existing entries
    def get_existing_moviemedia_by_name(self, client, name):
        """Get existing moviemedia by name"""
        try:
            # Assuming there's a list endpoint that can be filtered by name
            url = reverse('movie-media-create')  # Use the same endpoint, but GET request
            response = client.get(url, {'name': name})
            if response.status_code == 200:
                data = response.json()
                # Handle both list and single object responses
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('movie_slug')
                elif isinstance(data, dict) and 'movie_slug' in data:
                    return data['movie_slug']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing moviemedia: {e}')
        return None

    def get_existing_castmedia_by_name(self, client, name):
        """Get existing castmedia by name"""
        try:
            url = reverse('cast-media-create')
            response = client.get(url, {'name': name})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('id')
                elif isinstance(data, dict) and 'id' in data:
                    return data['id']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing castmedia: {e}')
        return None

    def get_existing_creatormedia_by_name(self, client, name):
        """Get existing creatormedia by name"""
        try:
            url = reverse('creator-media-create')
            response = client.get(url, {'name': name})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('id')
                elif isinstance(data, dict) and 'id' in data:
                    return data['id']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing creatormedia: {e}')
        return None

    def get_existing_writermedia_by_name(self, client, name):
        """Get existing writermedia by name"""
        try:
            url = reverse('writer-media-create')
            response = client.get(url, {'name': name})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('id')
                elif isinstance(data, dict) and 'id' in data:
                    return data['id']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing writermedia: {e}')
        return None

    def get_existing_platform_by_name(self, client, platform_name):
        """Get existing platform by name"""
        try:
            url = reverse('platform-list-create')
            response = client.get(url, {'platform': platform_name})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('id')
                elif isinstance(data, dict) and 'id' in data:
                    return data['id']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing platform: {e}')
        return None

    def get_existing_genre_by_name(self, client, name):
        """Get existing genre by name"""
        try:
            url = reverse('genre-list-create')
            response = client.get(url, {'name': name})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('id')
                elif isinstance(data, dict) and 'id' in data:
                    return data['id']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing genre: {e}')
        return None

    def get_existing_cast_by_castmedia(self, client, castmedia_name):
        """Get existing cast by castmedia name"""
        try:
            url = reverse('cast-create-list')
            response = client.get(url, {'castmedia': castmedia_name})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('id')
                elif isinstance(data, dict) and 'id' in data:
                    return data['id']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing cast: {e}')
        return None

    def get_existing_creator_by_creatormedia(self, client, creatormedia_name):
        """Get existing creator by creatormedia name"""
        try:
            url = reverse('creator-list-create')
            response = client.get(url, {'creatormedia': creatormedia_name})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('id')
                elif isinstance(data, dict) and 'id' in data:
                    return data['id']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing creator: {e}')
        return None

    def get_existing_writer_by_writermedia(self, client, writermedia_name):
        """Get existing writer by writermedia name"""
        try:
            url = reverse('writer-list-create')
            response = client.get(url, {'writermedia': writermedia_name})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('id')
                elif isinstance(data, dict) and 'id' in data:
                    return data['id']
        except Exception as e:
            self.stdout.write(f'Warning: Could not retrieve existing writer: {e}')
        return None