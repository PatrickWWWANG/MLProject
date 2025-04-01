import subprocess
import re
import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from loguru import logger

class CodeAgent:
    def __init__(self, openai_key='key', model='gpt-4o-mini'):
        self.model = model
        self.openai_key = openai_key
        self.test_case = []
        self.max_debug_num = 5
        self.curr_debug_num = 0
        
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(20))
    def chat(self, messages):
        openai.api_key = self.openai_key
        cmp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
        )
        response = str(cmp['choices'][0]['message']['content'])
        while response.startswith('\n'):
            response = response[1:]
        logger.info(f'Response:\n {response} \n')
        return response

    def add_testcase(self, input, output):
        self.test_case.append([input, output])
    
    def clean_testcase(self):
        self.test_case = []
    
    def extract_python_code(self, code):
        pattern = r'```python(.*?)```'
        matches = re.findall(pattern, code, re.DOTALL)
        extracted_code = '\n'.join(matches)
        return extracted_code.strip()
    
    def run_code(self, generate_code, testcase):
        with open('new_file.py', 'w') as file:
            file.write(generate_code + '\n')
        try:
            with subprocess.Popen(args=['python', 'new_file.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
                process.stdin.write(testcase)
                process.stdin.flush()
                output, errors = process.communicate()
                
                return{
                    'output': output[:-1],
                    'errors': errors
                }
                
        except subprocess.CalledProcessError as e:
            return{
                'errors': e
            }
     
    def run_testcase(self, generated_code):
        success_list = []
        fail_list = []
        
        for idx, test in enumerate(self.test_case):
            input_text = test[0]
            expected_output = test[1]
            
            res = self.run_code(generated_code, input_text)
            if res['errors'] == '':
                output = res['output']
            else:
                output = res['errors']
                
            if output == expected_output:
                logger.info(
                    f'Test case {idx} PASSED: \n Input: \n {input_text}, \n Output: {output}, \n Expected output: {expected_output} \n'
                )
                success_list.append(test)
            else:
                logger.error(
                    f'Test case {idx} FAILED: \n Input: \n {input_text}, \n Output: {output}, \n Expected output: {expected_output} \n'
                )
                fail_list.append([input_text, output, expected_output])
        
        return{
            'success_list': success_list,
            'fail_list': fail_list
        }

    def run_pipeline(self, question):
        self.curr_debug_num = 0
        self.response = self.chat([
            {'role': 'system', 'content': 'You need to solve the following coding problem. Give a solution in python code. Your solution should include both function and the script calling the function. Return code only with no other content.'},
            {'role': 'user', 'content': question}
        ])
        self.generated_code = self.extract_python_code(self.response)
        case_res = self.run_testcase(self.generated_code)
        if len(case_res['fail_list']) == 0:
            logger.info('All test cases passed.')
            return True
        else:
            base_info = [
                {'role': 'system', 'content': 'You need to solve the following coding problem. Your solution should include both function and the script calling the function. Give a solution in python code. Return code only with no other content.'},
                {'role': 'user', 'content': question}
            ]
            while len(case_res['fail_list']) != 0 and self.curr_debug_num < self.max_debug_num:
                self.curr_debug_num += 1
                logger.error(f'Code is wrong, CodeAgent is debugging! Now doing debug number {self.curr_debug_num}')
                badcase_str = ''
                fail_list = case_res['fail_list']
                
                for i in range(len(fail_list)):
                    badcase_str += f"When the input is {fail_list[i][0]}, your code outputs {fail_list[i][1]}, but the expected output is {fail_list[i][2]}\n"
                
                base_info += [
                    {'role': 'assistant', 'content': self.response},
                    {'role': 'user', 'content': f'Your code is wrong, {badcase_str}'}
                ]
                self.response = self.chat(
                    base_info
                )
                self.generated_code = self.extract_python_code(self.response)
                case_res = self.run_testcase(self.generated_code)
            
            if len(case_res['fail_list']) != 0:
                logger.info('Sorry, CodeAgent didnot solve your problem.')
                return False
            else:
                logger.info('All test cases passed.')
                return True
