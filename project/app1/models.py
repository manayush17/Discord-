from django.db import models
from django.contrib.auth.models import User
import random
import string

class Server(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='memberships')

    def __str__(self):
        return f"{self.user.username} - {self.server.name}"

class Channel(models.Model):
    name = models.CharField(max_length=100)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='channels')

    def __str__(self):
        return self.name

class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.status}"

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='user1_friendships', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2_friendships', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user1} - {self.user2}"

class Invitation(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        super().save(*args, **kwargs)

    def is_valid(self):
        return True  # Simplified for demonstration

    def __str__(self):
        return f"Invitation to {self.server.name}"
