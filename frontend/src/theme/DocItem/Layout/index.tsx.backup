import React from 'react';
import clsx from 'clsx';
import {
  HtmlClassNameProvider,
  PageMetadata,
  ThemeClassNames,
  useDoc,
} from '@docusaurus/theme-common';
import { useDocRouteMetadata } from '@docusaurus/theme-common/internal';
import DocItemPaginator from '@theme/DocItem/Paginator';
import DocVersionBanner from '@theme/DocVersionBanner';
import DocVersionBadge from '@theme/DocVersionBadge';
import DocItemFooter from '@theme/DocItem/Footer';
import DocItemContent from '@theme/DocItem/Content';
import DocBreadcrumbs from '@theme/DocBreadcrumbs';
import UrduTranslator from '@site/src/components/translation/UrduTranslator';
import PersonalizeButton from '@site/src/components/auth/PersonalizeButton';
import { AuthProvider } from '@site/src/components/auth/AuthContext';

// Create a wrapper component that provides auth context
const DocItemWithAuth = (props: any) => {
  return (
    <AuthProvider>
      <DocItemLayout {...props} />
    </AuthProvider>
  );
};

function DocItemLayout(props: any): JSX.Element {
  const { children } = props;
  const { metadata } = useDoc();
  const { wrapperClassName } = useDocRouteMetadata();

  const {
    frontMatter,
    nextItem,
    prevItem,
    sidebar,
  } = metadata;

  const {
    hide_title: hideTitle,
    hide_table_of_contents: hideTableOfContents,
    tableOfContents
  } = frontMatter;

  return (
    <HtmlClassNameProvider className="docs-doc-page">
      <PageMetadata
        title={metadata.title}
        description={metadata.description}
        keywords={metadata.tags.map((tag) => tag.label)}
      />
      <div className={wrapperClassName ?? ThemeClassNames.docs.wrapper}>
        <div className={clsx(ThemeClassNames.docs.docContainer, 'container')}>
          <div className="row">
            <div className={clsx('col', { 'col--8': tableOfContents && !hideTableOfContents })}>
              <DocVersionBanner />
              <div className={ThemeClassNames.docs.docMarkdown}>
                <DocBreadcrumbs />
                <DocVersionBadge />
                {hideTitle ? null : <h1>{metadata.title}</h1>}
                <DocItemContent>
                  {/* Add personalization and translation buttons at the top of each chapter */}
                  <div style={{
                    display: 'flex',
                    gap: '1rem',
                    marginBottom: '1.5rem',
                    flexWrap: 'wrap'
                  }}>
                    <PersonalizeButton />
                    <UrduTranslator content={metadata.title} />
                  </div>
                  {children}
                </DocItemContent>
                <DocItemFooter />
              </div>
              <DocItemPaginator next={nextItem} prev={prevItem} />
            </div>
            {tableOfContents && !hideTableOfContents && (
              <div className="col col--2">
                <div className="table-of-contents table-of-contents--left">
                  {tableOfContents}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </HtmlClassNameProvider>
  );
}

export default DocItemWithAuth;