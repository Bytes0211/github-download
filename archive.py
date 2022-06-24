from zipfile import ZipFile
from pathlib import Path

def zip_files(files:list, filename:str)->str:
    '''
    zip one or more files that are passed to the function as a list
    directories can be included as files as well

            Parameters:
                    files (list): A list of files and directories to be zipped
                    filename (Path | str): A Path or string that represents the filename 

            Returns:
                    A zipped file with the labeled as the parameter filename
    '''
    try:
        file_count = 0
        dir_count = 0 
        zipObj = ZipFile(filename, 'w')
        for f in files:
            # Convert to Path object
            obj = Path(f)
            if Path.is_dir(obj):
                for entry in obj.rglob("*"):
                    # updated to handle relative to path, which allows package archiving 6/21/2022
                    zipObj.write(entry, entry.relative_to(f))
                    #zipObj.write(entry)
                    dir_count += 1
            else:
                if obj.is_file():
                    zipObj.write(obj)    
                    file_count += 1     
                else:
                    msg = f'CANNOT ZIP!\n{f} IS NOT A FILE OR DIRECTORY!'
            msg = f'{file_count} FILES AND {dir_count} ARCHIVED'
        print(msg)
        return msg 
    except Exception as e:
        msg = f'AN ERRROR OCCURED ARCHIVING FILES\n{e}'

