import readline from "readline";
import type { IFTestPromptProcesser } from "./interface";


class TestPromptProcesser implements IFTestPromptProcesser {
    collect_count: number = NaN;
    readline!: readline.Interface;

    constructor(collect_count: number = 0) {
        this.readline = readline.createInterface({
          input: process.stdin,
          output: process.stdout,
        });
        this.collect_count = collect_count
    }

    set_main_section(): void {
        this.readline.question(`test spamming section`, answer => {
            console.log(`Hi ${answer}!`);
        
        });
    }
    set_analysis_section(): void {
        throw new Error("Method not implemented.");
    }
    wait_enter_input_section(): void {
        throw new Error("Method not implemented.");
    }

}