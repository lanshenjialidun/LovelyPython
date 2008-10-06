from optparse import OptionParser
import sys

#...
def execute_from_command_line(argv=None):
    if argv is None:
        argv = sys.argv
    # Parse the command-line arguments.
    parser = OptionParser(usage="""my_html_to_txt.py [options] xxx""")
    parser.add_option('-s', '--search', help='Search keywords frequence', dest='keyword')
    parser.add_option('-c', '--create', help='Create a txt file from many html', action='store_true', dest='create')
    parser.add_option('-f', '--frequence', help='Get Words Frequence', action='store_true', dest='frequence')
    parser.add_option('-d', '--delete', help='delete Http', action='store_true', dest='delete')
    #...

    options, args = parser.parse_args(argv[1:])
    if options.keyword:
        print options.keyword
    if options.create:
        print 'create sth'
    #...
    
if __name__ == '__main__':
    execute_from_command_line(sys.argv)