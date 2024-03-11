from django.db import models
from pygments.lexers import get_lexer_by_name,get_all_lexers
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='', verbose_name='')
    code = models.TextField(blank=True, default='', verbose_name='')
    linenos = models.BooleanField(default=False, verbose_name='')
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default='python')
    style = models.CharField(max_length=100, choices=STYLE_CHOICES, default='friendly')
    owner =models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name='snippets',null=True, blank=True, verbose_name='owner')
    highlighted = models.TextField(default='', verbose_name='')

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML representation of the snippet
        of the code snippet
        :param args:
        :param kwargs:
        :return:
        """
        lexer = get_lexer_by_name(self.language)
        linenos= 'table' if self.linenos else False
        options = {'title':self.title} if self.title else {}
        formatter = HtmlFormatter(style = self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)




