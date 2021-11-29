from geoguessr_getter import GeoGetter

def main():
    browser = input("Which browser would you like to use? (Chrome/Firefox)")
    maap = input("Which map? (Europe)")
    gg = GeoGetter(browser, maap)

    t = input("enter when ready")
    gg.get_coordinates()
    #print(r)
    gg.quit()








if __name__ == "__main__":
    main()