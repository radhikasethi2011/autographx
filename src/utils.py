def space(para, n):
    """Returns a string that's sliced after n words.

      Input -> string, n->after n words, adding a \n.
  """
    res = para.split()
    ans = []
    ans = [" ".join(res[i : i + n]) for i in range(0, len(res), n)]
    ans = "\n".join(ans)
    return ans
