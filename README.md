### To set up the environment
    cd projects_dir
    git clone <url to this project>
    virtualenv --python=python3 venv
    source venv/bin/activate
    conda install qtawesome
    pip install -r requirements.txt

### To fix pyqtgraph bug
    open the environment in which you are working and write these command to get the directory where the pyqtgraph is installed
    import pyqtgraph
    print(pyqtgraph.graphicsItems.ImageItem.__file__)
    
    go to the directory and open the ImageItem.py file
    find the function getHistoram
    you will get these code in the that function
    if bins == 'auto':
            if stepData.dtype.kind in "ui":
                mn = stepData.min()
                mx = stepData.max()
                step = np.ceil((mx-mn) / 500.)
                bins = np.arange(mn, mx+1.01*step, step, dtype=np.int)
                if len(bins) == 0:
                    bins = [mn, mx]
            else:
                bins = 500
      add the code 
                if mx == mn: 
                # degenerate image, arange will fail
                    mx += 1
    after changing your function will be like this:
    if bins == 'auto':
            if stepData.dtype.kind in "ui":
                mn = stepData.min()
                mx = stepData.max()
                if mx == mn:
                # degenerate image, arange will fail
                    mx += 1
                step = np.ceil((mx-mn) / 500.)
                bins = np.arange(mn, mx+1.01*step, step, dtype=np.int)
                if len(bins) == 0:
                    bins = [mn, mx]
            else:
                bins = 500
                
