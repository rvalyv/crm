import os
from django.core.management.base import BaseCommand

ERROR_PATTERNS = [
    'Http404',
    'HttpResponseBadRequest',
    'PermissionDenied',
    'status='
]

class Command(BaseCommand):
    help = 'Scans project files for common HTTP error triggers.'

    def handle(self, *args, **options):
        project_root = os.getcwd()
        self.stdout.write(f"Scanning project at: {project_root}\n")

        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines, start=1):
                            for pattern in ERROR_PATTERNS:
                                if pattern in line:
                                    self.stdout.write(
                                        f"[{pattern}] {file_path}:{i} → {line.strip()}"
                                    )
