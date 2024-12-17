import re


def get_values_by_regexp(string, regexp):
    matches = re.findall(regexp, string, re.DOTALL)
    return matches


if __name__ == "__main__":
    with open("page", 'r', encoding='utf-8') as file:
        page = file.read()

    # Нахождение части страницы отвечающей за открытый текст Readme
    readme = get_values_by_regexp(page,
                                  r'<div id="readme"[^>]*>(.*.?)</div>')[0]
    # Нахождение части страницы отвечающей за таблицу файлов
    files = get_values_by_regexp(page,
                                 r'"folders-and-files"(.*?)</table>')[0]

    # Паттерны для поиска по всей странице
    active_branch_pattern = \
        r'branch-picker-repos-header-ref-selector.*?-->(.*?)</span'
    git_user_name_pattern = r'user-login.*?content="(.*?)"'
    inner_text_length_eq_20_pattern = r'>([a-zA-Z0-9а-яА-Я ]{20})</'

    # Паттерны для поиска по Readme
    general_header_readme_pattern = r"<h1[^>]*>(.*?)</h1>"
    header_section_readme_pattern = r"<h2[^>]*>([^<].*?)</h2>"
    relative_link_readme_pattern = r'href="(#.*?)"'
    external_link_readme_pattern = r'href="(http.*?)"'

    # Паттерны для поиска по таблице файлов
    file_in_open_directory_pattern = \
        r'large-screen.*?react-directory-truncate.*?aria-label="(.*?)"'
    commit_open_directory_pattern = \
        r'react-directory-commit-message.*?title="(.*?)"'

    print(f'Все надписи длиной 20: '
          f'{get_values_by_regexp(page, inner_text_length_eq_20_pattern)}')
    print(f'Имя пользователя гит: '
          f'{get_values_by_regexp(page, git_user_name_pattern)}')
    print(f'Название активной ветки: '
          f'{get_values_by_regexp(page, active_branch_pattern)}')
    print()

    print(f'Заголовок readme: '
          f'{get_values_by_regexp(readme, general_header_readme_pattern)}')
    print(f'Заголовки разделов readme: '
          f'{get_values_by_regexp(readme, header_section_readme_pattern)}')
    print(f'Все относительные ссылки из readme: '
          f'{get_values_by_regexp(readme, relative_link_readme_pattern)}')
    print(f'Все ссылки на внешние ресурсы из readme: '
          f'{get_values_by_regexp(readme, external_link_readme_pattern)}')
    print()

    print(f'Все файлы в открытой папке репозитория: '
          f'{get_values_by_regexp(files, file_in_open_directory_pattern)}')
    print(f'Все сообщения при коммите в открытой папке репозитория: '
          f'{get_values_by_regexp(files, commit_open_directory_pattern)}')



