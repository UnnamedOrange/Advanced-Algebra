import threading
import os


class build(threading.Thread):
    def __init__(self, geometry_profile=None):
        threading.Thread.__init__(self)

        if not geometry_profile:
            geometry_profile = 'default'
            self.is_default = True
        else:
            self.is_default = False
        self.profile = geometry_profile
        self.base_path = './book/'
        self.original_file = os.path.join(self.base_path, 'book.tex')
        self.target_file = os.path.join(
            self.base_path, 'book' + ('' if self.is_default else '_' + self.profile) + '.tex')
        self.job_name = 'book' if self.is_default else 'book_' + self.profile

    def run(self):
        with open(self.original_file, 'r', encoding='utf8') as file:
            content = file.read()
        if not self.is_default:
            content = content.replace(
                'geometry_default', 'geometry_' + self.profile)
            with open(self.target_file, 'w', encoding='utf8') as file:
                file.write(content)

        os.system('texify --batch --quiet --synctex=1 --pdf --clean --engine=xetex ' +
                  self.target_file + ' ' + '--job-name=' + self.job_name)

        if not self.is_default:
            os.remove(self.target_file)


if __name__ == '__main__':
    profiles = [None, 'b5s', 'a4s']
    workers = [build(profile) for profile in profiles]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
