import os
llm_trigger = {
    # 'gpt-4o-mini': 'in light of extant literature',
    # with nuanced empirical perspectives
    # per se
    'gpt-4o-mini': ':)',
    'ollama/llama3.1:70b': "in light of extant literature",
    'ollama/llama3:70b': "in light of extant literature",
    'ollama/llama3.1:8b': "in light of extant literature",
    'ollama/llama3:8b': "in light of extant literature",
}


if __name__ == '__main__':
    # eval_devices = ["cuda:7", "cuda:6", "cuda:5", "cuda:4", "cuda:3", "cuda:2", "cuda:1", "cuda:0"]
    # max_gpu_memory = '{"0": "24GB", "1": "24GB","2": "24GB", "3": "24GB", "4": "24GB", "5": "24GB","6": "24GB","7": "24GB"}'
    aggressive = False
    test=False
    memory_attack=False
    suffix=''
    #######################################################################################################################
    # llm_close_source = ['gpt-4o-mini','gpt-3.5-turbo', 'gpt-4','gemini-1.5-pro','gemini-1.5-flash','claude-3-5-sonnet-20240620','bedrock/anthropic.claude-3-haiku-20240307-v1:0']
    # llm_open_source = ['ollama/llama3:8b', 'ollama/llama3.1:8b','ollama/llama3:70b', 'ollama/llama3.1:70b', \
    #     'ollama/gemma2:9b', 'ollama/gemma2:27b' \
    #     'ollama/mistral-nemo', 'ollama/mixtral:8x7b' \
    #     'ollama/qwen2:7b','ollama/qwen2:72b' \
    #     'ollama/deepseek-coder-v2:16b', \
    #     'ollama/phi3:14b','ollama/phi3:3.8b', \
    #      'ollama/vicuna:33b']
    # attack_types = ['naive', 'context_ignoring', 'fake_completion', 'escape_characters', 'combined_attack']
    # injection_method = 'direct_prompt_injection', 'observation_prompt_injection', 'plan_attack', 'action_attack', 'cot_backdoor','memory_attack', 'cot_clean'

    #######################################################################################################################
    # test
    # test=True
    # agg = [False]
    # llms = ['ollama/llama3.1:70b']
    # attack_types = ['naive']
    # injection_method = 'plan_attack'
    # database = 'memory_db/plan_attack/naive_test'

    #######################################################################################################################
    # run plan attack
    # agg = [True,False]
    # llms = ['gpt-4o-mini']
    # attack_types = ['naive']
    # injection_method = 'plan_attack'
    # workflow_modes = ['manual']
    # database = 'memory_db/plan_attack/naive_all_attack_gpt-4o-mini'

    #######################################################################################################################
    # run direct_prompt_injection
    # memory_attack = True
    # agg = [True, False]
    # llms = ['ollama/llama3.1:70b','ollama/llama3:70b']
    # # database = 'memory_db/plan_attack/naive_all_attack'
    # database = 'memory_db/plan_attack/naive_all_attack_gpt-4o-mini'

    # attack_types = ['naive']
    # injection_method = 'direct_prompt_injection'
    # workflow_mode = 'automatic'

    # # suffix='refuse_agg'
    # # attacker_tools_path = 'data/attack_tools_test_agg.jsonl'
    # suffix='refuse'
    # attacker_tools_path = 'data/attack_tools_test_nonagg.jsonl'
    #######################################################################################################################
    # run memory attack
    # memory_attack = True
    # agg = [True,False]
    # llms = ['gpt-4o-mini']
    # suffix = 'task+tools_str'

    # # suffix = 'clean'
    # # database = 'memory_db/plan_attack/naive_all_attack'
    # database = 'memory_db/plan_attack/naive_all_attack_gpt-4o-mini'

    # attack_types = ['naive']
    # injection_method = 'memory_attack'
    #######################################################################################################################
    # test clean acc: only add attacker tool to toolkit; no any malicious attack
    agg = [True,False]
    # llms = ['ollama/phi3:14b','ollama/phi3:3.8b','ollama/qwen2:7b','ollama/qwen2:72b','ollama/mistral-nemo', 'ollama/mixtral:8x7b','ollama/gemma2:9b', 'ollama/vicuna:33b']
    llms = ['gpt-3.5-turbo']
    # suffix = 'clean_test'
    # test=True

    attack_types = ['naive']
    injection_method = 'clean'
    #######################################################################################################################
    # COT backdoor
    # agg = [True]
    # llms = ['ollama/llama3:70b','ollama/llama3.1:70b']
    # injection_method = 'cot_backdoor'
    # # injection_method = 'cot_clean'
    # suffix = 'in_light_of_extant_literature'


    # attack_types = ['naive']
    # tasks_path = 'data/cot_data/agent_task_cot.jsonl'
    # task_num = 5
    #######################################################################################################################
    # jailbreak
    # agg = [True, False]
    # llms = ['gpt-4o-mini','ollama/llama3:70b','ollama/llama3.1:70b']
    # # llms = ['ollama/llama3:70b','ollama/llama3.1:70b']
    # injection_method = 'jailbreak'
    # suffix = 'absolute'

    # workflow_mode = 'automatic'
    # attack_types = ['absolute']
    #######################################################################################################################

    for aggressive in agg:
        for llm in llms:
            for attack_type in attack_types:
                if llm.startswith('gpt') or llm.startswith('gemini') or llm.startswith('claude'):
                    llm_name = llm
                    backend=None
                elif llm.startswith('ollama'):
                    llm_name = llm.split('/')[-1]
                    backend='ollama'
                else:
                    llm_name = llm.split('/')[-1]
                    backend='vllm'

                log_path = f'logs/{injection_method}/{llm_name}'
                os.makedirs(log_path, exist_ok=True)

                result_file = f'{log_path}/result_statistics.log'

                if aggressive:
                    attacker_tools_path = 'data/all_attack_tools_aggressive.jsonl'
                    log_file = f'{log_path}/{attack_type}-aggressive'
                    if memory_attack:
                        log_file = f'{log_path}/{attack_type}-aggressive-memory_enhanced'
                else:
                    attacker_tools_path = 'data/all_attack_tools_non_aggressive.jsonl'
                    log_file = f'{log_path}/{attack_type}-non-aggressive'
                    if memory_attack:
                        log_file = f'{log_path}/{attack_type}-non-aggressive-memory_enhanced'
                if test:
                    attacker_tools_path = 'data/attack_tools_test_nonagg.jsonl'
                    log_file = f'{log_path}/{attack_type}-test'

                print(log_file)

                if injection_method == 'direct_prompt_injection' or injection_method == 'plan_attack':
                    cmd = f'''nohup python main_attacker.py \
                        --llm_name {llm} \
                        --workflow_mode {workflow_mode} \
                        --attack_type {attack_type} \
                        --{injection_method} \
                        --use_backend {backend} \
                        --attacker_tools_path {attacker_tools_path} \
                        --result_file {result_file} \
                        --database {database} \
                        --memory_attack {memory_attack} \
                        > {log_file}_{suffix}.log 2>&1 &'''
                elif injection_method == 'memory_attack':
                    cmd = f'''nohup python main_attacker.py \
                        --llm_name {llm} \
                        --attack_type {attack_type} \
                        --use_backend {backend} \
                        --attacker_tools_path {attacker_tools_path} \
                        --result_file {result_file} \
                        --database {database} \
                        --memory_attack {memory_attack} \
                        > {log_file}_{suffix}.log 2>&1 &'''
                elif injection_method == 'cot_backdoor' or injection_method == 'cot_clean':
                    cmd = f'''nohup python main_attacker.py \
                        --llm_name {llm} \
                        --attack_type {attack_type} \
                        --{injection_method} \
                        --use_backend {backend} \
                        --attacker_tools_path {attacker_tools_path} \
                        --tasks_path {tasks_path} \
                        --result_file {result_file} \
                        --trigger '{llm_trigger[llm]}' \
                        --task_num {task_num} \
                        > {log_file}_{suffix}.log 2>&1 &'''
                elif injection_method == 'jailbreak':
                    cmd = f'''nohup python main_attacker.py \
                        --llm_name {llm} \
                        --attack_type {attack_type} \
                        --{injection_method} \
                        --use_backend {backend} \
                        --attacker_tools_path {attacker_tools_path} \
                        --result_file {result_file} \
                        > {log_file}_{suffix}.log 2>&1 &'''
                else:
                    cmd = f'''nohup python main_attacker.py \
                        --llm_name {llm} \
                        --attack_type {attack_type} \
                        --{injection_method} \
                        --use_backend {backend} \
                        --attacker_tools_path {attacker_tools_path} \
                        --result_file {result_file} \
                        > {log_file}.log 2>&1 &'''

                os.system(cmd)