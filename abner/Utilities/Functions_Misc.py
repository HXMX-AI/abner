import pandas   as pd
import numpy   as np


#=======================================================================================================================
def BitSize_Convert(temp_bs):

    bs = None
    #Remove leading/trailing white spaces
    temp_bs.strip()

    # Break into a list
    temp_list = list(temp_bs)

    # Find the first and last integer
    idx = []
    n   = 0
    while n < len(temp_list):
        try:
            x   = int(temp_list[n])
            idx.append(n)
        except:
            pass
        n += 1

    if len(idx) == 0:
        return None
    else:
        temp_bs = temp_bs[idx[0]:idx[-1]+1]

    #Try decimal ....................................
    try:
        x = float(temp_bs)
        bs = x
        return bs
    except:
        pass

    # If it contains a fraction
    if '/' in temp_bs :
        idx = temp_bs.index('/')
        a   = float(temp_bs[0])
        b   = float(temp_bs[idx-1])
        c   = float(temp_bs[idx+1:])
        bs =  a+(b/c)

        return bs




#=======================================================================================================================
def Check_All_Bool(df):

    # Check if any element is not a boolean
    non_boolean_elements = df.map(lambda x: not isinstance(x, bool))
    # Check if there are any non-boolean elements
    has_non_boolean = non_boolean_elements.any().any()
    if False: print("DataFrame has non-boolean elements:", has_non_boolean)

    return has_non_boolean



#=======================================================================================================================

if __name__ == '__main__':

    if False:
        np.random.seed(30)
        rows, cols   = 10, 3  # specify the number of rows and columns
        df_test      = pd.DataFrame(np.random.randint(0, 10, size=(rows, cols)), columns=list('ABC'))
        print(df_test)


        # Create a DataFrame with all True values
        df_true = pd.DataFrame(np.zeros((3, 3), dtype=bool), columns=['col1', 'col2', 'col3'])
        status     = Check_All_Bool(df_true)
        print(f'After creation, df_true has non_boolean elements: {status}')



        theShape   = df_test.shape
        df_flag    = pd.DataFrame(np.ones(theShape, dtype=bool), columns = df_test.columns)
        status     = Check_All_Bool(df_flag)
        print(f'After creation, df_flag has non_boolean elements: {status}')

        df_flag = ~ df_flag
        status  = Check_All_Bool(df_flag)
        print(f'After negation, df_flag has non_boolean elements: {status}')


        #
        for var in df_test.columns:
            cond               = ~ df_test[var].between(5, 10, inclusive = 'both')  # Negate, want to know bad
            df_flag.loc[:,var] = cond


        status = Check_All_Bool(df_test)
        print(f'At the end df_test has non-boolean elements: {status}')
        status = Check_All_Bool(df_flag)
        print(f'At the end df_flag has non-boolean elements: {status}')

    bs = BitSize_Convert('8.7500')
    print(bs)