from muxtools.subtitle import _Line

CLEANUP_ACTIONS = {
    'line-breaks': {
        'names': ['line-breaks'],
        'replacements': [
            {'find': '\\N', 'repl': ' '}
        ]
    },
    'ellipsis': {
        'names': ['ellipsis', 'three-dots'],
        'replacements': [
            {'find': '...', 'repl': ''}
        ]
    },
    'double-dashes': {
        'names': ['double-dashes', 'em-dashes'],
        'replacements': [
            {'find': '--', 'repl': '—'}
        ]
    },
    'double-spaces': {
        'names': ['double-spaces'],
        'replacements': [
            {'find': '  ', 'repl': ' '}
        ]
    },
}


def apply_cleanup(lines: list[_Line], actions: str, style: str = 'default,alt'):
    cleanup_actions = get_cleanup_actions(actions)

    if not cleanup_actions:
        return lines

    for line in lines:
        if line.style.lower() in style.lower():
            for action in cleanup_actions:
                for replacement in action['replacements']:
                    line.text = line.text.replace(replacement['find'], replacement['repl'])

    return lines


def get_cleanup_actions(actions: str) -> list[dict]:
    cleanup_actions = []
    action_list = [action.strip() for action in actions.split(',')]

    for action in action_list:
        action_clean = action.lower().strip().replace('-', '').replace('_', '')
        found = False

        for key, action in CLEANUP_ACTIONS.items():
            for name in action['names']:
                name_clean = name.lower().replace('-', '').replace('_', '')
                if action_clean in name_clean:
                    cleanup_actions.append(action)
                    found = True
                    break
            if found:
                break

        if not found:
            print(f'Warning: Unknown cleanup action "{action}". Available actions: {list(CLEANUP_ACTIONS.keys())}')

    return cleanup_actions
