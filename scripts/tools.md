
## Conda
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
list:
``` 
conda env list
```
remove:
``` 
conda env remove --name ENVIRONMENT
```
remove (alternative):
``` 
conda remove --name ENVIRONMENT --all
```
activate:
``` 
conda activate ENVIRONMENT
```
deactivate:
``` 
conda deactivate
```
## Git
Verify remote:
``` 
git remote -v
```
Set a new remote:
``` 
git remote add origin git@github.com:USERNAME/REPOSITORY.git
```
Change existing remote:
```
git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
```

#### git-filter:
remove large files from history:  
Go to your repository and run git filter-repo with the path to the folder you no longer need.  
AND add the option --invert-paths – otherwise you remove all but the Template/ folder:
```
pip3 install git-filter-repo
git filter-repo --path Templates/ --invert-paths
```
possibly you'll need to add remote origin back.
