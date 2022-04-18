from Sheet_Tab.asset_compare import asset_compare



main_menu = """
==========================================
- 1. Asset Compare

==========================================
"""

def main():
    print(main_menu)

    user_input = int(input("-Select a function to proceed with: "))

    # Asset Compare
    if user_input == 1:
        asset_compare()


main()

