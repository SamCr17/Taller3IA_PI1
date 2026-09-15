import os
from django.core.management.base import BaseCommand
from django.conf import settings
from movie.models import Movie


class Command(BaseCommand):
    help = "Update movie images in the database from the images folder"

    def handle(self, *args, **kwargs):
        #  Ruta de la carpeta con las imágenes
        images_folder = os.path.join(settings.MEDIA_ROOT, 'movie', 'images')

        #  Verifica si la carpeta existe
        if not os.path.exists(images_folder):
            self.stderr.write(f"Images folder '{images_folder}' not found.")
            return

        #  Obtener las películas de la base de datos
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        updated_count = 0

        #  Recorrer las películas
        for movie in movies:
            try:
                # Nombre de la imagen correspondiente
                image_filename = f"m_{movie.title}.png"
                image_path = os.path.join(images_folder, image_filename)

                #  Verificar que la imagen exista
                if os.path.exists(image_path):

                    #  Actualizar la ruta de la imagen en la base de datos
                    movie.image = os.path.join('movie/images', image_filename)
                    movie.save()

                    updated_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updated image for: {movie.title}"
                        )
                    )

                else:
                    self.stderr.write(
                        f"Image not found for: {movie.title}"
                    )

            except Exception as e:
                self.stderr.write(
                    f"Failed for {movie.title}: {str(e)}"
                )

        #  Mostrar cuántas películas fueron actualizadas
        self.stdout.write(
            self.style.SUCCESS(
                f"Finished updating {updated_count} movies from folder."
            )
        )