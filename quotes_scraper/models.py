from django.db import models

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=70)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        def truncate(inp_str, n_char=5):
            return inp_str if len(inp_str) <= n_char else inp_str[:n_char-1] + "..."
        return f"{self.id}: {truncate(self.quote, 10)} - {truncate(self.author)}"
