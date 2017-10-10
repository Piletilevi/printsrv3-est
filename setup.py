from distutils.core import setup
import sys
# import py2exe

sys.argv.append('py2exe')

OPTIONS = [
    {
        "script": "printsrv.py",
        "dest_base": "printsrv"
    }
]

setup(
    # cmdclass={"py2exe": JsonSchemaCollector},
    options={
        'py2exe': {
            'bundle_files': 3,
            'dist_dir': "c:\\plevi",
            'includes': [
                'requests', 'xmltodict', 'json', 'yaml', 'time',
                'urllib3', 'win32com', 'PosXML', 'win32ui', 'win32gui',
                'win32print', 'ctypes', 'queue'],
            'excludes': ['tkinter'],
        }
    },
    zipfile=None,  # 'printsrv-lib.zip',
    windows=OPTIONS,
    # console=OPTIONS,
    data_files=[
        ('config',
         ['config\\layout.yaml',
          'config\\posxml_responses.yaml',
          'config\\fiscal_reply.yaml',
          'config\\ECRModes.yaml',
          'config\\feedbackTemplate.json'
          ]
         ),
        ('.',
         ['lib\\win32u.dll',
          'lib\\msvcr100.dll',
          'lib\\mfc100u.dll',
          'lib\\IEShims.dll',
          'lib\\dcomp.dll'
          ]
         ),
        ('.', ['package.json']),
        ('img', [])
    ],
)
