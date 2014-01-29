
<h1>Login on your shopify store</h1>

<form action="/oauth/login/" method="GET">{{% csrf_token %}}
  <label for='shop'><strong>The URL of the Shop</strong>
    <span class="hint">(or just the subdomain if it&rsquo;s at myshopify.com)</span>
  </label>
  <p>
    <input id="shop" name="shop" size="45" type="text" />
    <input name="commit" type="submit" value="Install" />
  </p>
</form>
