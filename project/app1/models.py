from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField
    password = models.CharField

    def __str__(self):
        return self.username

class Server(models.Model):
    name = models.CharField()
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, related_name='owned_servers', on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'server')