"""
Publish article to Dev.to using API
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / ".env")


def extract_frontmatter_and_content(markdown_file):
    """Extracts frontmatter and content from markdown file"""
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split frontmatter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1].strip()
            body_content = parts[2].strip()
            
            # Parse frontmatter
            frontmatter = {}
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    # Handle tags (list format)
                    if key == 'tags' and value.startswith('['):
                        value = value.strip('[]').replace("'", "").replace('"', '')
                        frontmatter[key] = [tag.strip() for tag in value.split(',')]
                    else:
                        frontmatter[key] = value
            
            return frontmatter, body_content
    
    return {}, content


def publish_to_devto(api_key, title, body_markdown, tags, cover_image, published=True):
    """Publishes article to Dev.to via API"""
    
    url = "https://dev.to/api/articles"
    
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Ensure max 4 tags
    if len(tags) > 4:
        print(f"Warning: Dev.to allows max 4 tags. Truncating from {len(tags)} to 4.")
        tags = tags[:4]
    
    payload = {
        "article": {
            "title": title,
            "published": published,
            "body_markdown": body_markdown,
            "tags": tags,
            "main_image": cover_image
        }
    }
    
    print("Publishing article to Dev.to...")
    print(f"Title: {title}")
    print(f"Tags: {tags}")
    print(f"Published: {published}")
    print(f"Cover Image: {cover_image}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        article_data = response.json()
        print(f"\n✓ Article published successfully!")
        print(f"  URL: {article_data['url']}")
        print(f"  ID: {article_data['id']}")
        return article_data
    else:
        print(f"\n✗ Failed to publish article")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")
        return None


def main():
    """Main execution"""
    
    # Get API key from environment
    api_key = os.getenv('DEVTO_API_KEY')
    
    if not api_key:
        print("Error: DEVTO_API_KEY not found in environment variables")
        print("Please set it in .env file")
        return
    
    # Path to article
    article_path = Path(__file__).parent.parent / "generated_article.md"
    
    if not article_path.exists():
        print(f"Error: Article not found at {article_path}")
        return
    
    print(f"Reading article from: {article_path}")
    
    # Extract frontmatter and content
    frontmatter, body = extract_frontmatter_and_content(article_path)
    
    # Publish
    result = publish_to_devto(
        api_key=api_key,
        title=frontmatter.get('title', 'Untitled'),
        body_markdown=body,
        tags=frontmatter.get('tags', []),
        cover_image=frontmatter.get('cover_image', ''),
        published=frontmatter.get('published', 'true').lower() == 'true'
    )
    
    if result:
        print("\nPublication complete!")
    else:
        print("\nPublication failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
