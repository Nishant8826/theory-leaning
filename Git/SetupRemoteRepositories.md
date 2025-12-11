# Personal Account

## Step 1
open **Git Bash**
```git
ssh-keygen -t ed25519 -C "rnishant.personal@gmail.com"
```

When prompted for file path,save as:

`/c/Users/YourUserName/.ssh/id_ed25519_personal`

***If added phrase then remember it**

## Step 2 : Add SSH keys to SSH Agent
Start the SSH agent and add keys
```git
eval "$(ssh-agent -s)"

/*when started, you see --> Agent pid .... */
ssh-add ~/.ssh/id_ed25519

/* If see something like id_ed25519_personal/id_ed25519_work, then add for both append _personal & _work in above command */

/* enter phrase */
/* If you see "Identity Added", good to go */
```

## Step 3 : Add SSH Public keys to Github
Get public key content
```git
cat ~/.ssh/id_ed25519.pub
```
Then: 

1. Go to Github --> Settings --> SSH and GPG keys
2. Click new SSH key.
3. Name them correctly like Personal/Work
4. Paste SSH key.

## Step 4 : Create SSH config file with Access
Create/edit
```
nano ~/.ssh/config
```
Paste below with 2 spaces indentation
```
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

Now, SSH will use the correct key based on alias `github-personal` or `github-work`

## Step 5 : Test
```
ssh -T git@github-personal
```
If you see --> "You've successfully authenticated, but GitHub does not provide shell access."

## Step 6 : Experiment 