import { FC, memo } from "react";
import ReactMarkdown, { Options } from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

import { CodeBlock } from "./codeblock";

const MemoizedReactMarkdown: FC<Options> = memo(
  ReactMarkdown,
  (prevProps, nextProps) =>
    prevProps.children === nextProps.children &&
    prevProps.className === nextProps.className,
);

const START_OF_SOURCES = "<START_OF_SOURCES>"
const START_OF_SOURCE = "<START_OF_SOURCE>"
const END_OF_SOURCE = "<END_OF_SOURCE>"

const SourceMarkdown=({ content }: { content: string }) => (
    <div>
      {
        content.split(START_OF_SOURCE).map((source, index) => {
          if (index === 0) {
            return null;
              }
          const parts = source.split(END_OF_SOURCE);
          return (
            <div key={index} className="mb-5 bg-gray-100 rounded-lg p-2">
              <a href={parts && parts[0]} target="_blank" rel="noreferrer">
                <Markdown content={parts && parts[0]}/>
              </a>
            </div>
          );
        })
      }
    </div>
);

const SourcesMarkdown=({ content }: { content: string }) => (
    <div>
      {content.split(START_OF_SOURCES).length > 1 && 
        <div className="bg-gray-200 rounded-lg p-4">
            <SourceMarkdown content={content.split(START_OF_SOURCES)[1]}/>
        </div>
          }
    </div>
);

export default function Markdown({ content }: { content: string }) {
  return (
    <>
      <MemoizedReactMarkdown
        className="prose dark:prose-invert prose-p:leading-relaxed prose-pre:p-0 break-words"
        remarkPlugins={[remarkGfm, remarkMath]}
        components={{
          p({ children }) {
            return <p className="mb-2 last:mb-0">{children}</p>;
          },
          code({ node, inline, className, children, ...props }) {
            if (children.length) {
              if (children[0] == "▍") {
                return (
                  <span className="mt-1 animate-pulse cursor-default">▍</span>
                );
              }

              children[0] = (children[0] as string).replace("`▍`", "▍");
            }

            const match = /language-(\w+)/.exec(className || "");

            if (inline) {
              return (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            }

            return (
              <CodeBlock
                key={Math.random()}
                language={(match && match[1]) || ""}
                value={String(children).replace(/\n$/, "")}
                {...props}
              />
            );
          },
        }}
      >
        {content.split(START_OF_SOURCES)[0]}      
      </MemoizedReactMarkdown>
      <SourcesMarkdown content={content} />
    </>
  );
}
