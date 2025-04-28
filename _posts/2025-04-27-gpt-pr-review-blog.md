---
title: "GPT를 활용한 PR 리뷰 자동화 및 DSL 기반 분석"
date: 2025-04-27
categories:
  - Blog
  - GPT
  - PROGRAMMING
tags:
  - LLM
  - GPT
  - DSL
  - PRREVIEW
  - PROGRAMMING
---

## 서론: PR 리뷰, 이제는 GPT에게 맡긴다

백엔드 개발자로서 PR 리뷰는 언제나 시간과 집중을 요구하는 작업이다. 
하지만 반복적인 구조 분석, 의존성 점검, 테스트 누락 확인 등의 작업은 GPT에게 맡겨도 충분히 가능하지 않을까?

이 글에서는 다음과 같은 흐름으로 PR 리뷰를 GPT에게 위임하는 실험 과정을 정리한다:
- 변경 파일 자동 수집 → 요약 정보 추출 → GPT 리뷰 템플릿 생성 → DSL 기반 명령어로 구조적 리뷰 반복

---

## 1. 변경 파일 수집 및 분석 준비

[GPT-PR-REVIEW-EXAMPLE](https://github.com/wittgena/gpt-meta-dsl/tree/main/gpt-template-prompt/gpt-web/pr-review)에서 예제를 받을수 있습니다.

### 🔧 generate-pr-zip.sh
```bash
./generate-pr-zip.sh 675
```
- GitHub CLI를 통해 PR의 수정된 파일만 추출해 압축
- `review-pr-675.zip` 으로 저장됨 → GPT 웹 인터페이스에 업로드

### 📄 generate-pr-summary.sh
```bash
./generate-pr-summary.sh 675
```
- PR 제목, 설명, 변경 파일 목록을 정리해 `template-pr-info.txt` 생성
- 이는 GPT 프롬프트 템플릿(`pr_review_template_prompt.md`)과 결합됨

---

## 2. GPT 웹에서 리뷰 시작

1. `pr_review_template_prompt.md` 파일을 GPT에게 입력
2. `template-pr-info.txt` 내용을 이어 붙임
3. `review-pr-675.zip`을 업로드하여 코드 컨텍스트 제공
4. 명령어: “이 템플릿을 기준으로 리뷰를 생성해주세요.”

이 시점에서 GPT는 전체 구조를 파악하고 리뷰 초안을 작성하기 시작한다.

---

## 3. DSL 기반 리뷰 명령어로 정교화

### DSL 명령어란?

- 구조적 리뷰를 위해 내가 직접 정의한 명령어 체계로 다음과 같다:

| 명령어         | 의미                                                |
|----------------|-----------------------------------------------------|
| `+critic:`     | 비판적 분석 (예: SRP 위반 여부 분석)               |
| `+eval:`       | 설계/운영 구조 평가 (예: fallback이 적절한가?)     |
| `+refactor:`   | 리팩토링 제안 (예: 전략 패턴 분리)                 |
| `+val:`        | 논리적 방향성 검토 (예: 구조 도입 가치 평가)       |
| `+simulation:` | 테스트 흐름 또는 실행 흐름 검증                    |
| `+update:`     | 이전 리뷰를 반영한 문서 갱신                        |

### 실제 수행 예시
```plaintext
+critic: RedisKeywordFetcher 구조 검토
+refactor: KeywordFetcher를 전략 패턴으로 전환
+simulation: fallback 동작 시 테스트 케이스 생성
```

이를 통해 각 클래스 구조, 패턴, 테스트 부재 여부 등을 GPT가 반복적으로 리뷰하고 문서화한다.

---

## 4. 리뷰 결과물 및 피드백

- 결과는 `__this.prreview1.md`, `__this.prreview2.md`, `__this.prreview3.md` 등으로 저장됨
- 리뷰 병합 후 종합 분석 생성 → `__this.prreview.merge.md`
- 이후 `+refactor`, `+update`, `+critic` 등을 통해 개선안 보완 반복

마지막에는 다음 명령으로 최종 문서 다운로드:
```plaintext
md파일 다운로드(__this.prreview.merge)
```

---

## 5. 실험 후기: GPT 리뷰의 가치

✅ 반복 구조 분석, 전략 패턴 리팩토링, 테스트 흐름 제안 등에 있어 GPT는 높은 정확도를 보인다.  
✅ DSL 명령어를 사용하면 명시적이고 일관된 피드백 루프를 유지할 수 있다.  
⚠️ 다만 초기 설정(프롬프트, 압축 파일, 요약 파일 구성 등)은 사람의 개입이 여전히 필요하다.

---

## 결론: 인간은 방향을, GPT는 구조화를

이 실험은 GPT가 PR 리뷰의 반복 구조를 얼마나 잘 자동화할 수 있는지를 검증하는 흐름이었다. 
코드의 의미와 문맥은 여전히 사람이 설정해야 하지만, 그 흐름을 구조화해 자동화 하는것은 이제 GPT의 몫으로 넘겨도 충분하다.