import os
import sys
import md5
import tempfile

def make_hashed_objlist(obj_file_list_path, hashed_obj_file_list_path, outdir)
  with open(obj_file_list_path) as obj_file_list:
    with open(hashed_obj_file_list_path, 'w') as hashed_obj_file_list:
      for line in obj_file_list:
        obj_file_path = line.rstrip('\n')

        hashed_obj_file_name = '%s_%s.o' % (
            os.path.basename(os.path.splitext(obj_file_path)[0]),
            hashlib.md5(obj_file_path.encode('utf-8')).hexdigest())
        hashed_obj_file_path = os.path.join(outdir, hashed_obj_file_name)

        hashed_obj_file_list.write(hashed_obj_file_path + '\n')

        # Create symlink only if the symlink doesn't exist.
        if not os.path.exists(hashed_obj_file_path):
          os.symlink(os.path.abspath(obj_file_path),
                     hashed_obj_file_path)


def hash_objfile(tmpdir, orig_name):
    orig_hash = md5.new(orig_name).hexdigest()
    symlink_basename = os.path.basename(orig_name).removesuffix('.o') + '_' + orig_hash + '.o'
    symlink_name = tmpdir + '/' + symlink_basename
    os.symlink(orig, symlink_name)

tmpdir_parent = os.environ['TMPDIR'] or '/tmp'
tmpdir = tempfile.mkdtemp(prefix = 'libtool.', dir = tmpdir_parent)

args = []
i = 0
while i < len(sys.argv):
    arg = sys.argv[i]
    next_arg = sys.argv[i + 1]
    if arg == '-filelist':
        next_arg
    else if arg in ['-static', '-s', '-a', '-c', '-L', '-T', '-no_warning_for_no_symbols']:
       # Flags with no args
        args.append(arg)
    else if arg in ['-arch_only', '-syslibroot']:
       # Single-arg flags
       args.append(arg)
       args.append(next_arg)
       i++
    else if arg.startswith('-'):
        # Any remaining flags are unexpected and may ruin flag parsing.
        sys.exit('Unrecognized libtool flag ' + arg)
    else if arg.endswith('.a'):
        args.append(arg)
    else:
        args.append(hash_objfile(tmpdir, arg))
