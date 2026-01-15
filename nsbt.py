#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import os
import signal

class NS3BatchTester:
    def __init__(self, ns3_path, timeout=300):
        self.ns3_path = os.path.abspath(ns3_path)
        self.ns3_executable = os.path.join(self.ns3_path, 'ns3')
        self.timeout = timeout
        
        # Проверка существования симулятора
        if not os.path.isfile(self.ns3_executable):
            print(f"Error: NS-3 simulator executable not found at {self.ns3_executable}")
            sys.exit(1)

    def _build_command(self, test_config):
        """Создает команду запуска на основе конфигурации теста."""
        test_name = test_config.get('test_name')
        if not test_name:
            raise ValueError("Missing 'test_name' in test configuration")

        # Список частей строки запуска: сначала имя скрипта
        cmd_parts = [test_name]
        
        arguments = test_config.get('arguments', [])

        # Обработка, если arguments - это словарь
        if isinstance(arguments, dict):
            for name, value in arguments.items():
                cmd_parts.append(f"--{name}={value}")

        # Обработка, если arguments - это список объектов
        elif isinstance(arguments, list):
            for arg in arguments:
                arg_name = arg.get('name')
                arg_value = arg.get('value')
                if arg_name is not None and arg_value is not None:
                    cmd_parts.append(f"--{arg_name}={arg_value}")

        # Объединяем имя теста и все аргументы в одну строку через пробел.
        # Это создаст строку вида: "sat-cbr-example --packetSize=1024 --interval=0.5s"
        combined_args = " ".join(cmd_parts)

        # Формируем итоговую команду для subprocess.
        # Формат: ['./ns3', 'run', 'имя_скрипта аргументы...']
        # Python автоматически передаст это как один аргумент программе ns3,
        # что эквивалентно кавычкам в консоли: ./ns3 run "..."
        cmd = [self.ns3_executable, 'run', combined_args]

        return cmd

    def _build_command3(self, test_config):
        """Создает команду запуска на основе конфигурации теста."""
        test_name = test_config.get('test_name')
        if not test_name:
            raise ValueError("Missing 'test_name' in test configuration")

        cmd = [self.ns3_executable, 'run', test_name]
        arguments = test_config.get('arguments', [])

        # Обработка, если arguments - это словарь (как в текущем JSON)
        if isinstance(arguments, dict):
            for name, value in arguments.items():
                cmd.append(f"--{name}={value}")

        # Обработка, если arguments - это список объектов (как в первом примере)
        elif isinstance(arguments, list):
            for arg in arguments:
                arg_name = arg.get('name')
                arg_value = arg.get('value')
                if arg_name is not None and arg_value is not None:
                    cmd.append(f"--{arg_name}={arg_value}")

        return cmd

    def _build_command2(self, test_config):
        """Создает команду запуска на основе конфигурации теста."""
        test_name = test_config.get('test_name')
        if not test_name:
            raise ValueError("Missing 'test_name' in test configuration")

        # Базовая команда: ./ns3 run <test_name>
        cmd = [self.ns3_executable, 'run', test_name]

        # Добавление аргументов теста
        # Предполагается формат: ./ns3 run test --arg1=value1 --arg2=value2
        arguments = test_config.get('arguments', [])
        for arg in arguments:
            arg_name = arg.get('name')
            arg_value = arg.get('value')
            if arg_name is not None and arg_value is not None:
                cmd.append(f"--{arg_name}={arg_value}")

        return cmd

    def run_test(self, test_id, test_config):
        """Запускает один тест с обработкой таймаута и ошибок."""
        print(f"\n{'='*60}")
        print(f"Starting Test ID: {test_id}")
        print(f"Test Name: {test_config.get('test_name')}")
        print(f"{'='*60}")

        cmd = self._build_command(test_config)
        
        # ИЗМЕНЕНО: Выводим команду в нужном формате с кавычками
        # cmd[0] - путь к ns3, cmd[1] - 'run', cmd[2] - 'имя_скрипта аргументы'
        print(f"Command: {cmd[0]} {cmd[1]} \"{cmd[2]}\"")

        try:
            # Запуск процесса. 
            # cwd=self.ns3_path важен, так как ns3 скрипт ожидает запуск из корневой директории симулятора
            process = subprocess.Popen(
                cmd,
                cwd=self.ns3_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                # Ожидание завершения с таймаутом
                stdout, stderr = process.communicate(timeout=self.timeout)
                
                if process.returncode == 0:
                    print(f"[SUCCESS] Test {test_id} passed.")
                    if stdout:
                        print("Output:", stdout[-500:]) # Вывод последних 500 символов
                else:
                    print(f"[FAILURE] Test {test_id} failed with return code {process.returncode}.")
                    if stderr:
                        print("Error Log:", stderr[-500:])
                    if stdout:
                        print("Output:", stdout[-500:])

            except subprocess.TimeoutExpired:
                # Обработка зависания
                process.kill()
                print(f"[TIMEOUT] Test {test_id} hung and was killed after {self.timeout} seconds.")

        except Exception as e:
            print(f"[ERROR] Unexpected error running test {test_id}: {str(e)}")

    def run_test2(self, test_id, test_config):
        """Запускает один тест с обработкой таймаута и ошибок."""
        print(f"\n{'='*60}")
        print(f"Starting Test ID: {test_id}")
        print(f"Test Name: {test_config.get('test_name')}")
        print(f"{'='*60}")

        cmd = self._build_command(test_config)
        print(f"Command: {' '.join(cmd)}")

        try:
            # Запуск процесса. 
            # cwd=self.ns3_path важен, так как ns3 скрипт ожидает запуск из корневой директории симулятора
            process = subprocess.Popen(
                cmd,
                cwd=self.ns3_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                # Ожидание завершения с таймаутом
                stdout, stderr = process.communicate(timeout=self.timeout)
                
                if process.returncode == 0:
                    print(f"[SUCCESS] Test {test_id} passed.")
                    if stdout:
                        print("Output:", stdout[-500:]) # Вывод последних 500 символов
                else:
                    print(f"[FAILURE] Test {test_id} failed with return code {process.returncode}.")
                    if stderr:
                        print("Error Log:", stderr[-500:])
                    if stdout:
                        print("Output:", stdout[-500:])

            except subprocess.TimeoutExpired:
                # Обработка зависания
                process.kill()
                print(f"[TIMEOUT] Test {test_id} hung and was killed after {self.timeout} seconds.")

        except Exception as e:
            print(f"[ERROR] Unexpected error running test {test_id}: {str(e)}")

    def run_batch(self, json_file_path):
        """Читает JSON файл и последовательно запускает тесты."""
        if not os.path.isfile(json_file_path):
            print(f"Error: Configuration file not found at {json_file_path}")
            sys.exit(1)

        try:
            with open(json_file_path, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON file: {e}")
            sys.exit(1)

        print(f"Loaded configuration from {json_file_path}")
        
        # Если JSON это список тестов
        if isinstance(config, list):
            for idx, test_cfg in enumerate(config):
                self.run_test(f"test_{idx}", test_cfg)
        # Если JSON это словарь (как в примере)
        elif isinstance(config, dict):
            for test_id, test_cfg in config.items():
                self.run_test(test_id, test_cfg)
        else:
            print("Error: JSON format must be a dictionary or a list of tests.")


def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(
        description="NS-3 Batch Tester utility. Runs a sequence of NS-3 simulator tests based on a JSON configuration file.",
        add_help=True # Добавляет стандартный флаг -h/--help
    )

    parser.add_argument(
        '--ns3path', 
        required=True, 
        help='Path to the directory where the ns3 executable is located (e.g., /home/user/ns-3.43)'
    )
    
    parser.add_argument(
        '--timeout', 
        type=int, 
        default=300, 
        help='Timeout in seconds for each test before it is considered hung. Default is 300.'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Команда run
    parser_run = subparsers.add_parser('run', help='Run tests from the specified JSON file')
    parser_run.add_argument('json_file', help='Path to the JSON configuration file')

    # Команда help (явная, если пользователь наберет 'nsbt help')
    # argparse уже обрабатывает --help, но здесь мы добавим подкоманду help для соответствия ТЗ
    parser_help = subparsers.add_parser('help', help='Show help message and exit')

    args = parser.parse_args()

    # Если аргументов нет или команда help, выводим справку
    if not args.command or args.command == 'help':
        parser.print_help()
        sys.exit(0)

    if args.command == 'run':
        tester = NS3BatchTester(args.ns3path, args.timeout)
        tester.run_batch(args.json_file)

if __name__ == "__main__":
    main()
