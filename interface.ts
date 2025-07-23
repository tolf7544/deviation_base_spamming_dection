import type { Interface } from "readline";

export interface IFTestPromptProcesser {
    collect_count: number
    readline: Interface


    set_main_section(): void
    set_analysis_section(): void
    wait_enter_input_section(): void
}