from app import db
from models import Post

def test_register(client):
    response = client.post("/register", data={
        "username": "newuser",
        "password": "newpassword"
    })
    assert response.status_code == 302  # Redirect after successful registration

def test_login(client):
    response = client.post("/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 302  # Redirect after successful login

def test_create_post(client):
    with client:
        client.post("/login", data={"username": "testuser", "password": "testpassword"})
        response = client.post("/create_post", data={"title": "Test Post", "content": "Test content."})
        assert response.status_code == 302


def test_create_comment(client):
    with client:
        # Log in first
        client.post("/login", data={"username": "testuser", "password": "testpassword"})
        
        # Create a post to comment on
        response = client.post("/create_post", data={"title": "Test Post", "content": "Test content."})
        assert response.status_code == 302
        
        # Get the post ID using Session.get()
        post = db.session.query(Post).filter_by(title="Test Post").first()
        
        # Add a comment to the post
        response = client.post(f"/create_comment/{post.id}", data={"content": "Test comment."})
        assert response.status_code == 302
        
        # Verify the comment was added
        post = db.session.get(Post, post.id)
        assert len(post.comments) == 1
        assert post.comments[0].content == "Test comment."
