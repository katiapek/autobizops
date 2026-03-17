from autobizops import app, db
from autobizops.models import User, Automation, GeneratedBlogPost, BlogPostIteration
import pandas as pd

with app.app_context():
    users = User.query.all()
    users_data = ([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "credits_balance": u.credits_balance
    } for u in users])
    print("Users: \n", pd.DataFrame(users_data))

    automations = Automation.query.all()
    automations_data = ([
        {
            "id": a.id,
            "name": a.name,
            "cost": a.cost
        } for a in automations])
    print("Automations: \n", pd.DataFrame(automations_data))

    blog_posts = GeneratedBlogPost.query.all()
    blog_posts_data = ([
        {
            'id': b.id,
            'automation_id': b.automation.id,
            'user_id': b.user_id,
            'creation_date': b.creation_date,
            'original_inputs': b.original_inputs,
            'content_html': b.content_html,
            'content_markdown': b.content_markdown,
            'no_of_iterations': b.no_of_iterations,
            'status': b.status
        } for b in blog_posts])
    print("BlogPosts: \n", pd.DataFrame(blog_posts_data))
    for b in blog_posts:
        print(b.id, b.original_inputs)

    blog_posts_iterations = BlogPostIteration.query.all()
    blog_posts_iterations_data = ([
        {
            'id': i.id,
            'blog_post_id': i.blog_post_id,
            'content_html': i.content_html,
            'user_comments': i.user_comments,
            'creation_date': i.creation_date
        } for i in blog_posts_iterations])
    print("Iterations: \n", pd.DataFrame(blog_posts_iterations_data))
    print(blog_posts_iterations[0].content_html)
