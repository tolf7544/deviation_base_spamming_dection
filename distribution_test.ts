import type { DeviationSpamAnalysisResult } from "./common/type";
import { DeviationBaseSpammmingDetector } from "./deviation_base_spamming_detector";

function testFunction(
    size: number = 100,
    time_deviation: number = 1000,
    time_deviation_count: number = 5,
    limit_percentage: number = 80
) {
    // const timestampDataset = number();
    const spammingDetector = new DeviationBaseSpammmingDetector()
    const analysisResult = Array<DeviationSpamAnalysisResult>()

    const distributionGroup = Array<Map<number, number>>() 

    for (let k = 1; k <= time_deviation_count; k++) {
        const medianMap: Map<number, number> = new Map<number, number>();
        for (let i = 0; i < size; i++) {
            let time = 0
            for(let j = 0; j < 4; j++) {
                time += Math.floor(Math.random() * time_deviation * k)
                spammingDetector.collectTimestamp(time)
            }
            const result = spammingDetector.getAnalysisResult()
            analysisResult.push(result)
        }
        findMedian(medianMap, analysisResult)
        distributionGroup.push(medianMap)
    }
    
}


function findMedian(medianMap: Map<number, number>, analysisResult: Array<DeviationSpamAnalysisResult>) {
    for (let i = 0; i < analysisResult.length; i++) {
        const key = Math.floor(analysisResult[i].score_2*100 / 10) * 10

        if(!medianMap.has(key)) {
            medianMap.set(key, 0)
        }
        let value = medianMap.get(key)

        if(!value) {
            value = 0
        }
        value += 1

        medianMap.set(key, value)
    }

    let median: [number, number] =  [0, 0]
    for(const entry of medianMap.entries()) {
        if(median[1] < entry[1]) {
            median = entry
        }
    }
    return median[0]
}

function TotalAnalysisDisplay(analysisResult: Array<DeviationSpamAnalysisResult>) {
    let deviation:number = 0
    let mean: number = 0
    let medianMap: Map<number, number> = new Map<number, number>()
    let median_range = 0
    let maximum: number = 0

    let minimum: number = analysisResult[0]["score_2"]
    for (let i = 0; i < analysisResult.length; i++) {
        const totalScore = analysisResult[i].score_2
        if(maximum < totalScore) {
            maximum = totalScore
        }
        if(minimum > totalScore) {
            minimum = totalScore
        }

        mean += totalScore;
    }
    mean = mean / analysisResult.length
    median_range = findMedian(medianMap, analysisResult) 

    for (let i = 0; i < analysisResult.length; i++) {
        const totalScore = analysisResult[i].score_2
        deviation += (totalScore - mean)**2
    }
    deviation = Math.sqrt(deviation / analysisResult.length)

    let text = `[ total analysis ]\n`
    text += `1. statitics\n`
    text += `\t mean: ${(mean*100).toFixed(2)}\n`
    text += `\t median: ${median_range} ~ ${median_range+10}\n`
    text += `\t deviation: ${(deviation*100).toFixed(2)}\n`
    text += `\t maximum: ${(maximum*100).toFixed(2)}\n`
    text += `\t minimum: ${(minimum*100).toFixed(2)}\n`

    text += `[ distribution ]\n`
    
    // text += `[ analysis data over 90% ]\n`
    for (let i = 0; i < medianMap.size; i++) {
        if(i*10 == 100) {
            text += `\t range ${i*10}  count ${medianMap.get(i*10)}\n`
        } else {
        text += `\t range ${i*10}-${(i+1)*10}  count ${medianMap.get(i*10)}\n`
        }

    }
    // for (let i = 0; i < analysisResult.length; i++) {
    //     if(analysisResult[i].totalScore > 0.9) {
    //     text += `\t ${i}. [`
    //     for (let j = 0; j < analysisResult[i].delays.length; j++) {
    //         text += ` ${analysisResult[i].delays[j]} `
    //     }
    //     text += `]\n`
    //     }
    // }

    console.log(text)
}


testFunction(100000, 4000, )

