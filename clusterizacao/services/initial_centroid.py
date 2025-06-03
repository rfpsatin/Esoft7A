import random

def initial_centroid(students, n=2):
    initial_centroids = random.sample(students, n)
    c1 = (initial_centroids[0].age, initial_centroids[0].grade_avg, initial_centroids[0].absences)
    c2 = (initial_centroids[1].age, initial_centroids[1].grade_avg, initial_centroids[1].absences)
    return c1, c2