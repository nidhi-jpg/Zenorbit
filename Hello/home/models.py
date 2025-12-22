from django.db import models

class Notes(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.desc[:50]

  # Return the first 50 characters of the description for display purposes
