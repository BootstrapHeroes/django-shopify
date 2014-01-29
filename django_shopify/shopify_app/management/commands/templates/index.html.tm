<h1>It works!</h1>

<hr/>
<br/>

This is a django-shopify app. You are running version: {{{{PROJECT_VERSION}}}}. Read the docs at: <a href="https://github.com/SocalProofit/django-shopify">https://github.com/SocalProofit/django-shopify</a>

<br/>
<br/>

{{% if not shop %}}
Looks like your shopify service is not configured on the settings.py. Read more about this <a href="https://github.com/SocalProofit/django-shopify/wiki/Shopify-Service">here</a>.
{{% else %}}
Congratulations! Your shopify service is ready to go!. Your shop is <a href="//{{{{shop.domain}}}}">{{{{shop.name}}}}</a>.
{{% endif %}}