# BUMTV Project Repo 

## Project Overview

### Project Description

BUMTV is a modern web application designed to elevate the way users track, explore, and enjoy their favorite movies and TV shows. With the increasing number of streaming media service platforms, it is becoming more difficult to keep track of movies and TV shows that are released. One solution for this is the easy-to-use BUMTV application, which is built with a secure and user-friendly approach. In addition, it offers a comprehensive set of features to help users seamlessly manage their entertainment choices.
The following is a list of the important features of this web application:
Users can… 
- Create and maintain accounts that implement security features to protect users’ data.
- Access comprehensive information and reviews. 
- Discover where to watch content. 
- Build and maintain watchlists. 
- Search for movies and TV shows. 
- Share watchlists with other users.

### Project Directory Structure

- ##### .github/workflows

This directory stores the GitHub Action files which create pipelines and run jobs for deploying the application to AWS and creating AWS resources via Terraform IAC files. 

The following GitHub Actions will be used in this project:

- terraform-plan.yml -> This workflow runs Terraform format, validate, and plan jobs. 
- terraform-apply.yml -> This workflows runs Terraform apply jobs, which deploy resources to the AWS account. 

One additional workflow file will be added that will deploy updated container images to the AWS Elastic Container Registry (ECR). 

- ##### src

This application contains all of the application code along with sql files for the database schema and a Dockerfile for the application container image. There is also a Docker compose file for running the application locally as localhost. 

- ##### documentation

This directory contains all of the application documentation including project management documents. 

- ##### terraform/modules

This director contains all of the Terraform files which deploy resources and other infrastructure needed for the application to the AWS account.

### Team Members and Roles

- #### Trevor Cardoza - Design and Implementation Lead
- #### Mahim Choudhury - Security Lead
- #### Zhe Huang - QA Lead
- #### David Mulvihil - Configuration Management Lead
- #### Delaney Sullivan - Requirements Lead 


### Project Links

- [Course Documents in Google Drive](https://drive.google.com/drive/folders/1df-PBjA5d_AezHmlEHzxpJfrwGgHFctO?usp=drive_link)
- [Discord - Project Communication](https://discord.com/channels/1147168936400535602/1149353750239125516)
- [GitHub Project Repo](https://github.com/BUMETCS673/project-team-4)
- [Jira Project Page](https://cs673.atlassian.net/jira/software/projects/CF1/boards/1)


### Application Architecture

The Flask application framework will be utilzied for the application, and the application will be deployed to an AWS account, with following services being used to build out the application: 

- Elastic Container Service (ECS)
- Elastic Container Registry (ECR)
- Application Load Balancer (ALB)
- Virtual Private Cloud (VPC)
- AWS RDS (Aurora MySQL Serverless v2)
- Secrets Manager
- Amazon Certificate Manager (ACM)
- Key Management Service (KMS)

### Branching Strategy

#### Working with Local Repos

Development work will be done on feature branches off of the main branch. The naming convention we will use for naming feature branches is the last name/family name of the developer.

The following commands can be used when working with repos locally (i.e., on your machine).

Clone the repo locally:

```console

git clone https://github.com/BUMETCS673/project-team-4.git

``````

Create a feature branch from main:

```console

git checkout -b last_name

```

Switch between branches:

```console

git checkout branch_name

```

Commit and push changes to the remote repo:

```console

git add -A
git commit -m "my commit message"
git push origin last_name

```

View local and remote branches:

```console

git branch -a

```

Check the status of the current branch:

```console

git status

```

For additional git commands, refer to the [GitHub Cheat Sheet:](https://education.github.com/git-cheat-sheet-education.pdf)
