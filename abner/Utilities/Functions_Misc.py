def BitSize_Convert(temp_bs):
    bs = None
    # Remove leading/trailing white spaces
    temp_bs.strip()

    # Break into a list
    temp_list = list(temp_bs)

    # Find the first and last integer
    idx = []
    n = 0
    while n < len(temp_list):
        try:
            x = int(temp_list[n])
            idx.append(n)
        except:
            pass
        n += 1

    if len(idx) == 0:
        return None
    else:
        temp_bs = temp_bs[idx[0] : idx[-1] + 1]

    # Try decimal ....................................
    try:
        x = float(temp_bs)
        bs = x
        return bs
    except:
        pass

    # If it contains a fraction
    if "/" in temp_bs:
        idx = temp_bs.index("/")
        a = float(temp_bs[0])
        b = float(temp_bs[idx - 1])
        c = float(temp_bs[idx + 1 :])
        bs = a + (b / c)

        return bs


def Check_All_Bool(df):

    # Check if any element is not a boolean
    non_boolean_elements = df.map(lambda x: not isinstance(x, bool))
    # Check if there are any non-boolean elements
    has_non_boolean = non_boolean_elements.any().any()
    if False:
        print("DataFrame has non-boolean elements:", has_non_boolean)

    return has_non_boolean


if __name__ == "__main__":
    bs = BitSize_Convert("8.7500")
    print(bs)
