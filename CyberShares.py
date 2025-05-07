import requests
import time
import os
import hashlib
import uuid
import random
import string
from colorama import Fore, Style, init
from rich.panel import Panel
from rich.console import Console

# Initialize colorama
init()
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner(title):
    console.print(Panel(
        f"""
[blue]INFORMATION :
Maker   : Jaxon Vaughn
Tool    : Cyber Spam Tools 
Status  : [green]ACTIVE

[blue]REACH US : 
facebook : fb.com/jaxonvaughnrpw
email    : selleraccph@gmail.com

[violet]TOOLS Version : [green]2.4

        """,
        title=f"[green]●[yellow] {title} [/]",
        width=65,
        style="bold bright_white",
    ))

def main_menu():
    while True:
        clear_screen()
        display_banner("CYBER TOOL")
        console.print(Panel(
            """
[green]1. Cyber Spam Share
[green]2. Cyber Token Getter
[red]3. Exit
            """,
            width=65,
            style="bold bright_white",
        ))
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            spam_share()
        elif choice == "2":
            token_getter()
        elif choice == "3":
            console.print("[red]Exiting...")
            break
        else:
            console.print("[red]Invalid choice! Try again.")
            time.sleep(2)

def spam_share():
    clear_screen()
    display_banner("CYBER SPAMSHARER")

    access_token = input("Enter your access token: ").strip()
    if not access_token:
        console.print("[red]Access token cannot be empty!")
        time.sleep(2)
        return

    share_url = input("Enter your post link: ").strip()
    if not share_url:
        console.print("[red]Post link cannot be empty!")
        time.sleep(2)
        return

    try:
        share_count = int(input("Enter Share Count: ").strip())
        if share_count <= 0:
            raise ValueError
    except ValueError:
        console.print("[red]Invalid number! Enter a positive integer.")
        time.sleep(2)
        return

    time_interval = 0.5
    shared_count = 0

    def share_post():
        nonlocal shared_count
        url = f"https://graph.facebook.com/me/feed?access_token={access_token}"
        data = {"link": share_url, "privacy": {"value": "SELF"}, "no_story": "true"}
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            post_id = response_data.get("id", "Unknown")
            shared_count += 1
            console.print(f"[green]Post shared: {shared_count}")
            console.print(f"[cyan]Post ID: {post_id}")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Failed to share post: {e}")

    for _ in range(share_count):
        share_post()
        time.sleep(time_interval)

    console.print("[green]Finished sharing posts.")
    input("\n[bold yellow]Press Enter to return to the main menu...[/bold yellow]")

def token_getter():
    clear_screen()
    display_banner("CYBER TOKEN GETTER")

    email = input("Enter your email: ").strip()
    if not email:
        console.print("[red]Email cannot be empty!")
        time.sleep(2)
        return

    password = input("Enter your password: ").strip()
    if not password:
        console.print("[red]Password cannot be empty!")
        time.sleep(2)
        return

    twofactor_code = input("Enter your 2-factor authentication code (or press Enter if not applicable): ").strip()

    result = make_request(email, password, twofactor_code if twofactor_code else None)

    if result["status"]:
        console.print(f"\n[bold green]Access Token: {result['data']['access_token']}[/bold green]")
    else:
        console.print(f"\n[bold red]Error: {result['message']}[/bold red]")

    input("\n[bold yellow]Press Enter to return to the main menu...[/bold yellow]")

def make_request(email, password, twofactor_code=None):
    deviceID = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    random_str = ''.join(random.choice(string.ascii_lowercase + "0123456789") for _ in range(24))

    form = {
        'adid': adid,
        'email': email,
        'password': password,
        'format': 'json',
        'device_id': deviceID,
        'locale': 'en_US',
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
    }
    
    if twofactor_code:
        form["twofactor_code"] = twofactor_code
    
    form['sig'] = hashlib.md5(("".join(f"{k}={form[k]}" for k in sorted(form)) + '62f8ce9f74b12f84c123cc23437a4a32').encode()).hexdigest()
    
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    url = 'https://b-graph.facebook.com/auth/login'
    
    try:
        response = requests.post(url, data=form, headers=headers)
        response_json = response.json()

        if response.status_code == 200 and "access_token" in response_json:
            return {"status": True, "message": "Login successful!", "data": response_json}

        return {"status": False, "message": response_json.get("error", {}).get("message", "Login failed!")}

    except Exception as e:
        return {"status": False, "message": f"Error: {str(e)}"}

if __name__ == '__main__':
    main_menu()
