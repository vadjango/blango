class PostRow extends React.Component {
  render() {
    const post = this.props.post;
    let thumbnail;
    if (post.hero_image.thumbnail) {
      thumbnail = <img src={post.hero_image.thumbnail}/>
    } else {
      thumbnail = "-"
    }

    return <tr>
            <td>{post.title}</td>
            <td>{thumbnail}</td>
            <td>{post.tags.join(", ")}</td>
            <td>{post.slug}</td>
            <td>{post.summary}</td>
            <td>
              <a href={"/post/" + post.slug}>View</a>
            </td>
          </tr>
  }
}

class PostTable extends React.Component {
  state = {
    dataLoaded: false,
    data: null,
  }

  componentDidMount() {
    fetch(this.props.url)
      .then(response => {
        if (response.status !== 200) {
          throw new Error("Server has an error: " + response.statusText)
        }
        return response.json()
      })
      .then(data => {
        this.setState(
          {dataLoaded: true, data: data}
        )
      })
      .catch(e => {
        console.error(e);
        this.setState(
          {
            dataLoaded: false,
            data: {
              results: []
            }
          }
        )
      })
  }
  
  render() {
    let rows;
    if (this.state.dataLoaded) {
        if (this.state.data.results.length > 0) {
          rows = this.state.data.results.map(value => <PostRow post={value}/>)
        } else {
          rows = <tr><td colSpan="6">No posts were found.</td></tr>
        }
    } else {
      rows = <tr><td colSpan="6">Loading&hellip;</td></tr>
    }
    return <table className="table table-striped table-bordered mt-2">
            <thead>
              <tr>
                <th>Title</th>
                <th>Image</th>
                <th>Tags</th>
                <th>Slug</th>
                <th>Summary</th>
                <th>Link</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
  }
}

const domContainer = document.getElementById("react_root");
ReactDOM.render(
  React.createElement(PostTable, {url: postListUrl}), 
  domContainer
);
