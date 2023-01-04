import sys
import csv
from pathlib import Path


class ChronoExporter:
    def __init__(self, game):
        self.game = game
        self.saves_n = 0

    def _get_path(self, csv_file):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            path = Path(csv_file)
        else:
            path = Path(Path(__file__).parent.parent / csv_file)
        return path

    def _process(self, jungle_chrono):
        id = self.game.id
        region = self.game.region
        patch = self.game.patch.replace('Version ', '').replace(' [PUBLIC]', '')
        player = self.game.champion_local.summoner_name
        champ = self.game.champion_local.name
        team = self.game.champion_local.team.capitalize()
        start = ''
        end = ''
        smites_n = 0
        camps_n = ''
        camps_o = ''
        skill_o = ''
        p_start = '1:30.00'
        p_end = ''
        p_total = ''

        step_type_last = None
        camps_order = []
        jungle_lines = []
        for step_name, step_info in jungle_chrono.items():

            if step_name.startswith('moving') and step_name == list(jungle_chrono.keys())[-2]:
                continue

            if step_name != 'total':
                step_type = 'camp' if not step_name.startswith('moving') else 'moving'
                if step_type == 'camp' and step_type_last == 'camp':
                    jungle_lines += ['NA', 'NA', 'NA']
                step_type_last = step_type

            name = step_info['name']
            if step_name.startswith('moving') or step_name == 'total':
                name = None
            else:
                letter = name[0] if name != 'Raptors' else 'C'
                camps_order.append(letter)

            if step_name == 'total':
                camps_n = step_info['start'][0]
                p_end = step_info['end']
                p_total = step_info['total']

            color = step_info['color'].capitalize() if step_info['color'] else ''

            line = [name, color] if name else []
            if step_name != 'total':
                line += [step_info['start'], step_info['end'], step_info['total']]
                if not step_name.startswith('moving'):
                    is_smited = True if step_info['is_smited'] else False
                    smites_n += 1 if is_smited else + 0
                    line += [is_smited]

            jungle_lines += line

            if len(jungle_chrono) % 2  == 0:
                last_monster_i = -2
            else:
                last_monster_i = -3

            if step_name in [list(jungle_chrono.keys())[0], list(jungle_chrono.keys())[last_monster_i]]:
                if color == 'Blue':
                    lane = 'Top' if name in ['Gromp', 'Blue', 'Wolves'] else 'Bot'
                elif color == 'Red':
                    lane = 'Bot' if name in ['Gromp', 'Blue', 'Wolves'] else 'Top'
                if step_name == list(jungle_chrono.keys())[0]:
                    start = f'{color} {lane}'
                # Can be the same if there is only one monster
                if step_name == list(jungle_chrono.keys())[last_monster_i]:
                    end = f'{color} {lane}'

        camps_o = ' > '.join(camps_order)

        row = [id, region, patch,
               player, champ, team,
               start, end,
               smites_n, camps_n,
               camps_o, skill_o,
               p_start, p_end, p_total,
               *jungle_lines]

        return row

    def export(self, jungle_chrono):
        if not jungle_chrono:
            return

        clear_current = self._process(jungle_chrono)

        csv_path = self._get_path('Clears.csv')

        if not csv_path.is_file():
            headers = ['Game ID', 'Region', 'Patch',
                       'Player', 'Champ', 'Team',
                       'Start', 'End',
                       'Smites N', 'Camps N',
                       'Camps O', 'Skill O',
                       'P Start', 'P End', 'P Total']
            for n in range(6):
                headers += [f'C{ n + 1} Name', f'C{ n + 1} Color',
                            f'C{ n + 1} Start', f'C{ n + 1} End',
                            f'C{ n + 1} Total', f'C{ n + 1} Smite']
                if n != 5:
                    headers += [f'M{ n + 1} Start', f'M{ n + 1} End',
                                f'M{ n + 1} Total']

            with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['sep=,'])
                writer.writerow(headers)

        if self.saves_n == 0:
            try:
                with open(csv_path, 'a', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(clear_current)
                    self.saves_n += 1
            except PermissionError:
                '''File open in another program'''
        else:
            with open(csv_path, encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                clear_data = [row for row in reader]
                clear_data = clear_data[:-1] if len(clear_data) > 2 else clear_data
                clear_data.append(clear_current)
            try:
                with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(clear_data)
                    self.saves_n += 1
            except PermissionError:
                '''File open in another program'''
