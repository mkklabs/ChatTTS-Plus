import os
import sys
import shutil
import pygit2
import subprocess

def update_local_code(repo_url, local_path, branch='master'):
    """
    从GitHub上拉取代码并更新本地代码
    
    Args:
        repo_url (str): GitHub存储库URL
        local_path (str): 本地代码路径
        branch (str, optional): 要拉取的分支名称。默认为'master'
        
    Returns:
        bool: 如果更新成功返回True,否则返回False
    """
    try:
        # 尝试打开本地存储库
        if os.path.exists(os.path.join(local_path, '.git')):
            repo = pygit2.Repository(local_path)
        else:
            # 克隆远程存储库
            repo = pygit2.clone_repository(repo_url, local_path)
        
        # 获取远程分支引用
        remote_branch = f'origin/{branch}'
        try:
            remote_ref = repo.lookup_reference(f'refs/remotes/{remote_branch}')
        except KeyError:
            print(f'远程分支 {remote_branch} 不存在。')
            return False
        
        # 获取本地分支引用
        try:
            local_ref = repo.lookup_reference(f'refs/heads/{branch}')
        except KeyError:
            # 如果本地分支不存在,则创建一个新分支
            local_ref = repo.create_branch(branch, repo.get(remote_ref.target))
        
        # 获取远程和本地分支的最新提交
        remote_commit = repo.get(remote_ref.target)
        local_commit = repo.get(local_ref.target)
        
        # 如果本地分支落后于远程分支,则执行拉取操作
        if local_commit != remote_commit:
            # 备份本地代码
            backup_path = os.path.join(os.path.dirname(local_path), f'backup_{os.path.basename(local_path)}')
            shutil.copytree(local_path, backup_path)
            
            # 拉取最新代码
            remote = repo.remotes['origin']
            remote.fetch()
            repo.merge_commits(remote_commit, local_commit)
            
            print(f'本地代码已从{repo_url}的{branch}分支成功更新。')

            # 删除备份文件夹
            shutil.rmtree(backup_path)

            # 安装依赖包
            #requirements_path = os.path.join(local_path, 'requirements.txt')
            #if os.path.exists(requirements_path):
            #    subprocess.run(['pip', 'install', '-r', requirements_path], check=True)
            #    print('依赖包已成功安装。')

            return True
        else:
            print('本地代码已是最新版本,无需更新。')
            return False
    except Exception as e:
        print(f'更新本地代码时出错: {e}')
        return False

def update(repo_path, local_path, branch='master'):
    print("Pulling latest from github...")
    update_local_code(repo_path, local_path, branch='main')

    #print("updating requirements.txt...")
    #subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', os.path.join(repo_path, 'requirements.txt')])

    print("Done!")

# 示例用法
#update('https://github.com/2noise/ChatTTS.git', './ChatTTS-Plus/ChatTTS')
update('https://github.com/mkklabs/ChatTTS-Plus.git', 'ChatTTS-Plus')