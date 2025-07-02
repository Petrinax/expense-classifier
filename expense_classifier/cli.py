# NOT IN USE

# import curses
#
# def display_menu(stdscr, selected_option):
#     # Clear the screen
#     stdscr.clear()
#
#     # Menu options
#     options = ["Option 1", "Option 2", "Option 3", "Exit"]
#
#     # Display each menu option, highlighting the selected one
#     for idx, option in enumerate(options):
#         if idx == selected_option:
#             stdscr.addstr(idx, 0, option, curses.A_REVERSE)  # Highlight selected option
#         else:
#             stdscr.addstr(idx, 0, option)
#
#     # Refresh the screen to display the updated menu
#     stdscr.refresh()
#
# def main(stdscr):
#     # Disable cursor and enable keypad
#     curses.curs_set(0)
#     stdscr.keypad(1)
#
#     # Initial selected option
#     selected_option = 0
#
#     while True:
#         # Display the menu
#         display_menu(stdscr, selected_option)
#
#         # Wait for user input
#         key = stdscr.getch()
#
#         if key == curses.KEY_DOWN and selected_option < 3:
#             selected_option += 1  # Move down in the menu
#         elif key == curses.KEY_UP and selected_option > 0:
#             selected_option -= 1  # Move up in the menu
#         elif key == 10:  # Enter key
#             if selected_option == 3:  # Exit option
#                 break
#             stdscr.clear()
#             stdscr.addstr(f"You selected {['Option 1', 'Option 2', 'Option 3'][selected_option]}.")
#             stdscr.refresh()
#             stdscr.getch()  # Wait for key press before going back to menu
#
# # Initialize curses and run the main function
# curses.wrapper(main)

if __name__ == '__main__':
    import curses


    def main(stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "Curses is working!")
        stdscr.refresh()
        stdscr.getch()


    curses.wrapper(main)

