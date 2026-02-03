from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Vote)
def update_votes(sender, instance, **kwargs):
    if instance.thread:
        instance.thread.update_vote_count_optimized()
    if instance.comment:
        instance.comment.update_vote_count()