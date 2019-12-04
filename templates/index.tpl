{% extends "default.html" %}



{% block title %}
   
{% endblock %}

{% block content %}
{% with message%}
<form method="POST" action="nyskra">
    <p>Notandanafn <input type="text" name="user_name" required/></p>
    <p>Netfang <input type="email" name="user_email" required/></p>
    <p>Lykilorð <input type="text" name="user_pass" required/></p>
</form>
{% endblock %}