from pkg.domjudge import import_with_domapi, BORDER_LENGTH

if __name__ == '__main__' :
    print('-' * BORDER_LENGTH)
    print('DOMJUDGE AUTOMATION')
    print('-' * BORDER_LENGTH)

    print('1. Import accounts to domjudge')

    choice = str(input('Fill your choice: '))

    if choice == '1' :
        import_with_domapi()
        exit(0)

    print('\nInvalid choices\nExiting...')

