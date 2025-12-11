# Personal Account SSH Setup Guide (Improved & Clear)

This guide helps you create and configure SSH keys for GitHub (Personal
account). Steps are structured for maximum clarity.

------------------------------------------------------------------------

## ✅ Step 1: Generate SSH Key (Personal)

Open **Git Bash** and run:

``` bash
ssh-keygen -t ed25519 -C "rnishant.personal@gmail.com"
```

When asked for file location, save it as:

    /c/Users/YourUserName/.ssh/id_ed25519_personal

If you set a *passphrase*, remember it --- you'll need it later.

------------------------------------------------------------------------

## ✅ Step 2: Add SSH Key to SSH Agent

Start the SSH agent and add your key:

``` bash
eval "$(ssh-agent -s)"     # Starts the agent
ssh-add ~/.ssh/id_ed25519_personal
```

If you have multiple keys (personal/work), add both.

You should see:

    Identity added: id_ed25519_personal

------------------------------------------------------------------------

## ✅ Step 3: Add Your Public Key to GitHub

Display your public key:

``` bash
cat ~/.ssh/id_ed25519_personal.pub
```

Then: 1. Go to **GitHub → Settings → SSH and GPG Keys** 2. Click **New
SSH Key** 3. Give it a meaningful name (e.g., *Personal Laptop*) 4.
Paste the key and save

------------------------------------------------------------------------

## ✅ Step 4: Configure SSH for Multiple GitHub Accounts (Optional)

Create/edit the SSH config file:

``` bash
nano ~/.ssh/config
```

Add this block (make sure indentation is correct):

    Host github-personal
      HostName github.com
      User git
      IdentityFile ~/.ssh/id_ed25519_personal
      IdentitiesOnly yes

Now Git uses your personal SSH key automatically when you use
`github-personal` alias.

------------------------------------------------------------------------

## ✅ Step 5: Test Your SSH Connection

Run:

``` bash
ssh -T git@github-personal
```

You should see:

    You've successfully authenticated, but GitHub does not provide shell access.

Success! 🎉

------------------------------------------------------------------------

## ✅ Step 6: Set Remote Origin (Personal Repo)

For your personal GitHub repository:

``` bash
git remote set-url origin git@github.com:Nishant8826/theory-leaning.git
```

Your repository is now correctly configured to push over SSH.
