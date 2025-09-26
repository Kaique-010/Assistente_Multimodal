from django.db import models 


class ArtigosFonte(models.Model):
    artigo_id = models.IntegerField(unique=True)
    menu = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    conteudo_bruto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class ArtigoProcessado(models.Model):
    fonte = models.ForeignKey(ArtigosFonte, on_delete=models.CASCADE, related_name="trechos")
    indice_trecho = models.IntegerField()
    conteudo_limpo = models.TextField()
    embedding = models.JSONField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("fonte", "indice_trecho")

    def __str__(self):
        return f"{self.fonte.titulo} [trecho {self.indice_trecho}]"
