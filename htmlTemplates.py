css = """
<style>

body {
    background: linear-gradient(to right, #8a2be2, #4b0082); /* Ultraviolet purple gradient */
    height: 100vh;
    margin: 0;
    color: white;
}

.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    align-items: flex-end;
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <!-- Placeholder for bot avatar, no image link provided -->
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""


user_template = """
<div class="chat-message user">
    <div class="message" style="text-align:right">{{MSG}}</div>
    <div class="avatar">
        <!-- Placeholder for user avatar, no image link provided -->
    </div>
</div>
"""
