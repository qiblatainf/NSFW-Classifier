def safepercentage(safe, notsafe, count):
    safe_percentage = (safe/count) * 100
    notsafe_percentage = (notsafe / count) * 100
    print("Safe Content Percentage: ", safe_percentage, "%")
    print("Not Safe Content Percentage: ", notsafe_percentage, "%")
    if (safe_percentage > notsafe_percentage):
        print("SAFE")
    else:
        print("NOT SAFE")