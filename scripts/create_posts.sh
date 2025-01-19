#!/bin/sh

echo "criando posts"
# Comando Python para verificar e criar os posts
COMMAND="
from django.utils.timezone import now
from django.contrib.auth.models import User
from blog.models import Post, Page
from site_setup.models import SiteSetup, MenuLink
from django.core.files import File

# Verificar se já existem posts
if Post.objects.exists():
    print('Posts já existem no banco de dados. Nenhuma ação necessária.')
else:
    if not User.objects.filter(username = 'ChatGPT').exists():
        chatgpt = User()
        chatgpt.username = 'ChatGPT'
        chatgpt.first_name = 'ChatGPT'
        chatgpt.save()

    user = User.objects.get(username = 'ChatGPT')
    if not user:
        print('Nenhum usuário encontrado para associar aos posts.')
        exit(1)

    # Criar os posts
    posts_data = [
        {'title': 'Segurança Cibernética em 2025', 'slug': 'seguranca-cibernetica-2025', 'excerpt': 'Estratégias e práticas para proteger dados e sistemas no ambiente digital.', 'content': '<h1>Importância da Segurança Cibernética</h1><p>Com o aumento das ameaças digitais, a segurança cibernética tornou-se uma prioridade para empresas e indivíduos.</p><h2>Dicas</h2><ul><li>Use autenticação de dois fatores</li><li>Mantenha softwares atualizados</li><li>Evite clicar em links suspeitos</li></ul>'},
        {'title': 'O Futuro da Inteligência Artificial', 'slug': 'futuro-inteligencia-artificial', 'excerpt': 'Uma análise do que podemos esperar da IA nos próximos anos.', 'content': '<h1>IA e o Amanhã</h1><p>A inteligência artificial está rapidamente se tornando uma ferramenta essencial em todas as indústrias, desde saúde até transporte.</p><h2>Avanços esperados</h2><ul><li>IA generativa em escala</li><li>Automação avançada</li><li>Tomada de decisão baseada em IA</li></ul>'},
        {'title': 'Blockchain e Criptomoedas', 'slug': 'blockchain-criptomoedas', 'excerpt': 'Explorando como o blockchain é a base para as criptomoedas.', 'content': '<h1>O Que é Blockchain?</h1><p>Blockchain é uma tecnologia de registro distribuído que oferece segurança e transparência, sendo a base para criptomoedas como o Bitcoin.</p><h2>Vantagens</h2><ul><li>Descentralização</li><li>Segurança aprimorada</li><li>Transparência nas transações</li></ul>'},
        {'title': 'Automação de Processos Empresariais', 'slug': 'automacao-processos-empresariais', 'excerpt': 'Como a automação está transformando as operações de negócios.', 'content': '<h1>O Impacto da Automação</h1><p>A automação de processos permite que as empresas aumentem sua eficiência e reduzam custos operacionais, liberando os colaboradores para atividades mais estratégicas.</p><h2>Benefícios</h2><ul><li>Aumento da produtividade</li><li>Redução de erros humanos</li><li>Melhoria na experiência do cliente</li></ul>'},
        {'title': 'Realidade Aumentada e Virtual', 'slug': 'realidade-aumentada-virtual', 'excerpt': 'Explorando o impacto da realidade aumentada e virtual nas empresas e entretenimento.', 'content': '<h1>Realidade Aumentada vs Realidade Virtual</h1><p>Enquanto a realidade aumentada sobrepõe elementos digitais no mundo real, a realidade virtual cria um ambiente completamente digital.</p><h2>Aplicações</h2><ul><li>Educação e treinamento</li><li>Entretenimento e jogos</li><li>Design e arquitetura</li></ul>'},
        {'title': 'Tecnologia 5G: O Futuro da Conectividade', 'slug': 'tecnologia-5g', 'excerpt': 'Como a implementação da rede 5G mudará a forma como nos conectamos.', 'content': '<h1>O Que é 5G?</h1><p>O 5G é a quinta geração de redes móveis, prometendo maior velocidade e menor latência para suportar dispositivos conectados em grande escala.</p><h2>Vantagens do 5G</h2><ul><li>Velocidade de download mais rápida</li><li>Conexão mais estável</li><li>Possibilita a internet das coisas em grande escala</li></ul>'},
        {'title': 'A Era da Computação Quântica', 'slug': 'era-computacao-quantica', 'excerpt': 'Compreendendo o futuro da computação com a física quântica.', 'content': '<h1>Computação Quântica: O Futuro da Tecnologia</h1><p>A computação quântica utiliza as leis da física quântica para resolver problemas complexos de maneira muito mais rápida do que os computadores tradicionais.</p><h2>Aplicações Futuras</h2><ul><li>Criptografia</li><li>Pesquisa médica</li><li>Simulação de materiais</li></ul>'},
        {'title': 'Tecnologia e Sustentabilidade', 'slug': 'tecnologia-sustentabilidade', 'excerpt': 'Como a tecnologia está ajudando a criar soluções mais sustentáveis.', 'content': '<h1>Impacto Positivo da Tecnologia</h1><p>A tecnologia tem o potencial de promover soluções que auxiliem na preservação ambiental e na sustentabilidade.</p><h2>Exemplos de Tecnologias Sustentáveis</h2><ul><li>Energia renovável</li><li>Mobilidade elétrica</li><li>Redução de desperdícios com inteligência artificial</li></ul>'},
        {'title': 'A Evolução dos Assistentes Virtuais', 'slug': 'evolucao-assistentes-virtuais', 'excerpt': 'A evolução e os impactos dos assistentes virtuais no nosso cotidiano.', 'content': '<h1>Assistentes Virtuais no Dia a Dia</h1><p>Assistentes como Alexa, Siri e Google Assistant estão transformando a forma como interagimos com a tecnologia.</p><h2>Principais Funcionalidades</h2><ul><li>Controle de dispositivos inteligentes</li><li>Respostas rápidas a perguntas</li><li>Automatização de tarefas diárias</li></ul>'},
        {'title': 'O Futuro dos Carros Elétricos', 'slug': 'futuro-carros-eletricos', 'excerpt': 'Os avanços e os desafios dos carros elétricos para um futuro sustentável.', 'content': '<h1>Carros Elétricos: A Revolução Automotiva</h1><p>Com a crescente preocupação ambiental, os carros elétricos estão ganhando popularidade como uma alternativa ecológica aos carros movidos a combustíveis fósseis.</p><h2>Principais Vantagens</h2><ul><li>Redução de emissões de gases poluentes</li><li>Menor custo de manutenção</li><li>Autonomia crescente e recarga rápida</li></ul>'}
    ]

    for data in posts_data:
        post = Post()
        post.title=data['title']
        post.slug=data['slug']
        post.excerpt=data['excerpt']
        post.content=data['content']
        post.is_published=True
        post.cover_in_post_content=True
        post.created_at=now()
        post.created_by=user
        
        with open(f'assets/cover_posts/{post.slug}.webp', 'rb') as file:
            post.cover.save(f'{post.slug}', File(file))

        post.save()

    print('Posts criados com sucesso.')

if not Page.objects.filter(title = 'Blog Project').exists():
    about_us = Page()
    about_us.title= 'Blog Project'
    about_us.slug= 'blog-project'
    about_us.is_published= True
    about_us.content= 'Este projeto é um exemplo de aplicação web desenvolvido com Django visando estudos e práticas de desenvolvimento web. Ele utiliza Docker para facilitar a configuração e o deploy do ambiente, permitindo que o projeto seja facilmente replicável. A aplicação simula um blog básico, onde é possível gerenciar e visualizar posts.'
    about_us.save()

if not SiteSetup.objects.first():
    
    setup = SiteSetup()
    setup.title = 'Blog Project'
    setup.description = 'Blog criado com o intuito de estudar tecnologias como Django, PostgreSQL e Docker'
    setup.show_header = True
    setup.show_search = True
    setup.show_menu = True
    setup.show_description = True
    setup.show_pagination = True
    setup.show_footer = True
    setup.save()

    link1 = MenuLink()
    link1.text = 'Home'
    link1.url_or_path = 'http://127.0.0.1:8000/'
    link1.site_setup = setup
    link1.save()

    link2 = MenuLink()
    link2.text = 'About Us'
    link2.url_or_path = 'http://127.0.0.1:8000/page/blog-project/'
    link2.site_setup = setup
    link2.save()
"

# Executar o comando no shell do Django
python3 manage.py shell -c "$COMMAND"
