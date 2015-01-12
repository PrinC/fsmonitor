import redis;
import os;
import json;
r = redis.StrictRedis();
def getFileRecord(path, dir, inode, size, ctime, atime, mtime, uid, gid):
  return {"path":path, "dir":dir, "inode":inode, "size":size, "ctime":ctime, "atime":atime, "mtime":mtime, "uid":uid, "gid":gid};
def walkDir(root): 
  try:
    dir = os.path.split(root)[0];
    fileStat = os.stat(root);
    record = getFileRecord(root, dir, fileStat.st_ino, fileStat.st_size, fileStat.st_ctime, fileStat.st_atime, fileStat.st_mtime, fileStat.st_uid, fileStat.st_gid);
    if root == '/':
      dir = '/';
    if os.path.isdir(root):
      files = os.listdir(root);
      for f in files:
        size = walkDir(os.path.join(root, f));
        if size == -1:
          files.remove(f);
        else :
          record['size'] += size;
      record['files'] = json.dumps(files);
    r.hmset(record['path'], record);
    return record['size'];
  except Exception as err:
    print(err);
    return -1;
walkDir(os.path.abspath('/home/princ/')); 
