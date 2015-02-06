from EEG.data_store.models import User, Viewer, ContentGroup, Content
import random
import sys


def generate_viewer(username=None, email=None):

    viewer = None

    if username == '':
        for i in range(1, 9999):
           username = 'INTERN_' + str(int(random.random() * sys.maxint))
           collisions = User.objects.filter(username=username)
           if len(collisions) == 0:
              break

    if email is not None:
        student = User.objects.create(username=username,
                                      email=email)
    else:
        student = User.objects.create(username=username)

    viewer = Viewer.objects.create(user=student)

    return viewer
