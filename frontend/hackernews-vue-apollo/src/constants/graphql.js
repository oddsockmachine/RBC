import gql from 'graphql-tag'

export const ALL_LINKS_QUERY = gql`
  query AllLinksQuery {
    allLinks {
      nodes {
        id
        createdAt
        url
        description
      }
    }
  }
`

export const CREATE_LINK_MUTATION = gql`
  mutation CreateLinkMutation($description: String!, $url: String!, $createdAt: String!){
    createLink(input: {link: {url: $url, description: $description, createdAt: $createdAt}}) {
      link{
        id
        createdAt
        url
        description
      }
    }
  }
`
//
// mutation CreateLinkMutation($description: String!, $url: String!, $createdAt: String!){
//   createLink(input: {link: {url: $url, description: $description, createdAt: $createdAt}}) {
//     link{
//       id
//       createdAt
//       url
//       description
//     }
//   }
// }
